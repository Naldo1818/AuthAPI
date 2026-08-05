from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import HTTPAuthorizationCredentials

from app.security import security
from app.config import supabase


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

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