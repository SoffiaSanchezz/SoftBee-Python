# from fastapi import FastAPI, Depends
# from sqlalchemy.orm import Session
# from app.infraestructure.database.database import SessionLocal
# from app.infraestructure.api.endpoints import user

# app = FastAPI()
# app.include_router(user.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def read_root(db: Session = Depends(get_db)):
#     return {"message": "¡Conexión a la base de datos usando .env y database.py exitosa!"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infraestructure.api.endpoints import user

app = FastAPI()

# Configura CORS para permitir peticiones desde Flutter (emulador o dispositivos)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://10.0.2.2:8000",  # IP emulador Android
    "*",  # para pruebas, permite todos (recomiendo restringir en producción)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "¡API funcionando correctamente!"}
