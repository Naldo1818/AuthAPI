from fastapi import Header, HTTPException

from app.config import supabase


def get_current_user(authorization: str = Header(default=None)):

    # Check Authorization header exists
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    # Check Bearer prefix
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    # Extract token
    token = authorization.replace("Bearer ", "")

    try:
        response = supabase.auth.get_user(token)

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return response.user