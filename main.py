from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers
from app.infraestructure.api.endpoints import user
app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a SoftBee API"}