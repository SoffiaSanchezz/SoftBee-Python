# # app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configura tus claves secretas y tiempos de expiración
SECRET_KEY = "tu_clave_secreta_aca"  # Usa algo más seguro en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración del token

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


