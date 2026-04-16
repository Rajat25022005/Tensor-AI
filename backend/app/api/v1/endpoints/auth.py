"""Authentication endpoints — register, login, token refresh."""

from fastapi import APIRouter

from app.models.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="User login")
async def login(request: LoginRequest) -> TokenResponse:
    """Authenticate a user and return a JWT."""
    # TODO: wire up user service
    return TokenResponse(access_token="stub", token_type="bearer")


@router.post("/register", summary="Register a new user")
async def register() -> dict[str, str]:
    """Register a new user account."""
    # TODO: wire up user service
    return {"message": "Registration endpoint stub"}
