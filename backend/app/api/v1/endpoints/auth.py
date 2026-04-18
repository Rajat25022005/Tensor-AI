"""Authentication endpoints — register, login, logout, me."""

from fastapi import APIRouter, Response, Request, HTTPException, status
from pydantic import BaseModel, Field

from app.core.config import settings
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token
from app.core.logging import logger

router = APIRouter()

# ── In-memory user store (replace with a real database in production) ────────
_users_db: dict[str, dict] = {
    "admin@tensorai.dev": {
        "id": "1",
        "email": "admin@tensorai.dev",
        "name": "Tensor Admin",
        "role": "admin",
        "hashed_password": hash_password("admin1234"),
    }
}

COOKIE_KEY = "tensorai_session"


# ── Request / Response schemas ───────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=4, description="User password")


class RegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
    name: str = Field(..., min_length=1, description="Display name")


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str


# ── Helper ───────────────────────────────────────────────────────────────────

def _get_current_user(request: Request) -> dict:
    """Extract and validate the user from the session cookie."""
    token = request.cookies.get(COOKIE_KEY)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    subject = decode_access_token(token)
    user = _users_db.get(subject)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/login", summary="User login")
async def login(credentials: LoginRequest, response: Response) -> dict:
    """Authenticate a user and set an httpOnly JWT cookie."""
    user = _users_db.get(credentials.email)

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        logger.warning("auth.login.failed", email=credentials.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=user["email"])

    response.set_cookie(
        key=COOKIE_KEY,
        value=token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    logger.info("auth.login.success", email=user["email"])
    return {"message": "Successfully logged in"}


@router.post("/register", summary="Register a new account")
async def register(data: RegisterRequest, response: Response) -> dict:
    """Register a new user account."""
    if data.email in _users_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    import uuid
    user_id = str(uuid.uuid4())[:8]

    _users_db[data.email] = {
        "id": user_id,
        "email": data.email,
        "name": data.name,
        "role": "user",
        "hashed_password": hash_password(data.password),
    }

    token = create_access_token(subject=data.email)

    response.set_cookie(
        key=COOKIE_KEY,
        value=token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    logger.info("auth.register.success", email=data.email, user_id=user_id)
    return {"message": "Account created successfully"}


@router.post("/logout", summary="User logout")
async def logout(response: Response) -> dict:
    """Clear the httpOnly JWT cookie."""
    response.delete_cookie(key=COOKIE_KEY)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse, summary="Get current user")
async def get_me(request: Request) -> UserResponse:
    """Return the currently authenticated user's profile."""
    user = _get_current_user(request)
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
    )
