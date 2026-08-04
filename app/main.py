from fastapi import FastAPI
from app.config import supabase

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "API Running"
    }


@app.on_event("startup")
def startup():
    print("Connected to Supabase")