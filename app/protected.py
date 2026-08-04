from fastapi import APIRouter, Header, HTTPException, status
from app.config import supabase

router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)

@router.get("/profile")
async def profile(authorization: str = Header(default=None)):

    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token required"
        )

    parts = authorization.split()

    if len(parts) != 2 or parts[0] != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = parts[1]

    try:
        response = supabase.auth.get_user(token)

        return {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": response.user.created_at
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )