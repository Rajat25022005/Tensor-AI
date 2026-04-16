"""Authentication endpoints — register, login, logout, me."""

from fastapi import APIRouter, Response, Depends, HTTPException, status
from pydantic import BaseModel

class LoginCredentials(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/login", summary="User login")
async def login(credentials: LoginCredentials, response: Response) -> dict[str, str]:
    """Authenticate a user and set an httpOnly JWT cookie."""
    # TODO: Validate credentials in database
    
    # Simulate token generation
    token = "demo_jwt_token_stub"
    
    # Set httpOnly cookie
    response.set_cookie(
        key="tensorai_session",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=86400  # 1 day
    )
    
    return {"message": "Successfully logged in"}

@router.post("/logout", summary="User logout")
async def logout(response: Response) -> dict[str, str]:
    """Clear the httpOnly JWT cookie."""
    response.delete_cookie(key="tensorai_session")
    return {"message": "Successfully logged out"}

@router.get("/me", summary="Check current user session")
async def check_session() -> dict[str, str]:
    """Check if the session cookie is valid. For demo, it always returns success if called."""
    # TODO: Verify token from cookie and fetch DB user
    return {"id": "1", "email": "admin@tensorai.dev", "role": "admin"}
