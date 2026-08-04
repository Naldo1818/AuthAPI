from fastapi import APIRouter, HTTPException, status
from app.models import UserCredentials
from app.config import supabase

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(credentials: UserCredentials):

    # Check for empty values
    if not credentials.email.strip() or not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )

        return {
            "message": "User created successfully.",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login")
async def login(credentials: UserCredentials):

    if not credentials.email.strip() or not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required."
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )

        return {
            "message": "Login successful.",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )