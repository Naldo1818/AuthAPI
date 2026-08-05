from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException

from app.config import supabase

router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


@router.get("/profile")
def profile(authorization: str = Header(default=None)):

    # -----------------------
    # Step 1
    # Check header exists
    # -----------------------

    if authorization is None:

        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    # -----------------------
    # Step 2
    # Check Bearer prefix
    # -----------------------

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    # -----------------------
    # Step 3
    # Remove "Bearer "
    # -----------------------

    token = authorization.replace("Bearer ", "")

    # -----------------------
    # Step 4
    # Verify token with Supabase
    # -----------------------

    try:

        response = supabase.auth.get_user(token)

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # -----------------------
    # Step 5
    # Check user exists
    # -----------------------

    if response.user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    # -----------------------
    # Step 6
    # Return profile
    # -----------------------

    return {

        "id": response.user.id,

        "email": response.user.email,

        "created_at": response.user.created_at

    }