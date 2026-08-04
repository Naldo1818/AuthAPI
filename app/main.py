from fastapi import FastAPI
from app.auth import router as auth_router
from app.public import router as public_router

app = FastAPI(
    title="Authentication API",
    description="Assignment API using FastAPI and Supabase",
    version="1.0.0"
)

# Register the public routes
app.include_router(public_router)

# Register the authentication routes
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Authentication API is running"}