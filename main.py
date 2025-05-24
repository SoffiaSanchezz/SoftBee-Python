# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infraestructure.api.endpoints import user

app = FastAPI()

allow_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://10.0.2.2:8000",
    "http://127.0.0.1:8000",
    "*",  # menos seguro
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye tus routers
app.include_router(user.router)
