"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.services.lifecycle import startup_handler, shutdown_handler
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    setup_logging()
    await startup_handler()
    yield
    await shutdown_handler()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="TensorAI — Autonomous Business Intelligence Platform API",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan,
)

# ── Middleware (order matters: outermost first) ──────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=200, window_seconds=60)

# ── Routes ───────────────────────────────────────────────────────────────────

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# ── Socket.IO integration ───────────────────────────────────────────────────

try:
    import socketio

    sio = socketio.AsyncServer(
        async_mode="asgi",
        cors_allowed_origins=settings.CORS_ORIGINS,
        logger=False,
    )

    @sio.event
    async def connect(sid, environ):
        """Handle Socket.IO client connection."""
        pass

    @sio.event
    async def disconnect(sid):
        """Handle Socket.IO client disconnection."""
        pass

    @sio.on("query")
    async def handle_query(sid, data):
        """Handle real-time query via Socket.IO."""
        from app.core.dependencies import get_orchestrator

        question = data.get("question", "")
        if not question:
            await sio.emit("error", {"message": "Empty question"}, to=sid)
            return

        orchestrator = get_orchestrator()
        result = await orchestrator.run(query=question)

        await sio.emit("query_result", result, to=sid)

    # Mount Socket.IO as an ASGI sub-application
    socket_app = socketio.ASGIApp(sio, other_app=app)

except ImportError:
    # python-socketio not installed — run without WebSocket support
    socket_app = None
