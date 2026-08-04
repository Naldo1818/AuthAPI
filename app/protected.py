from fastapi import APIRouter, Header, HTTPException, status

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

    return {
        "message": "Authorization header received.",
        "authorization": authorization
    }