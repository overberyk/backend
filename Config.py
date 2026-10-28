# Config.py
"""
Configuración central de la aplicación: base de datos, seguridad (hash de
contraseñas y JWT) y parámetros generales. Según el estándar del PDF,
Config.py agrupa configuración de BD, variables de entorno y claves de
configuración.
"""

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# --- Rate limiting ---

limiter = Limiter(key_func=get_remote_address)

# --- Base de datos ---

databaseUrl = os.getenv("DATABASE_URL")
if not databaseUrl:
    raise RuntimeError("DATABASE_URL no está configurada")

connectArgs = {}
if databaseUrl.startswith("mysql"):
    connectArgs = {"ssl": {}}
elif databaseUrl.startswith("sqlite"):
    connectArgs = {"check_same_thread": False}

engine = create_engine(databaseUrl, pool_pre_ping=True, connect_args=connectArgs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Parámetros generales de la aplicación ---

appTitle = "API E-commerce"
appDescription = "API para gestión E-Commerces."
appVersion = "0.1.0"

corsOrigins: list[str] = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173",  # por defecto pruebas locales
).split(",")

adminEmail = os.getenv("ADMIN_EMAIL")
adminPassword = os.getenv("ADMIN_PASSWORD")


# --- Seguridad: hashing de contraseñas ---

def hashPassword(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verifyPassword(passwordPlain: str, passwordHash: str) -> bool:
    return bcrypt.checkpw(passwordPlain.encode("utf-8"), passwordHash.encode("utf-8"))


# --- Seguridad: JWT ---

secretKey = os.getenv("JWT_SECRET_KEY")
if not secretKey:
    raise RuntimeError(
        "JWT_SECRET_KEY no está configurada. Define una clave larga y "
        "aleatoria (por ejemplo con `openssl rand -hex 32`) antes de "
        "arrancar la API."
    )
if len(secretKey) < 32:
    raise RuntimeError(
        "JWT_SECRET_KEY es demasiado corta (mínimo 32 caracteres). "
        "Genera una nueva con `openssl rand -hex 32`."
    )

algorithm = "HS256"
# Access token de vida corta: si se filtra, la ventana de uso es pequeña.
accessTokenExpireMinutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
# Refresh token de vida larga: se usa solo para pedir nuevos access tokens.
refreshTokenExpireDays = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))


def createAccessToken(data: dict, expiresDelta: Optional[timedelta] = None) -> str:
    toEncode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expiresDelta or timedelta(minutes=accessTokenExpireMinutes)
    )
    toEncode.update({"exp": expire, "type": "access"})
    return jwt.encode(toEncode, secretKey, algorithm=algorithm)


def decodeAccessToken(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secretKey, algorithms=[algorithm])
    except JWTError:
        return None
    # Un refresh token no debe poder usarse como access token.
    if payload.get("type") != "access":
        return None
    return payload


def generateRefreshToken() -> str:
    """Genera un string aleatorio y seguro para usar como refresh token."""
    return secrets.token_urlsafe(64)


def hashRefreshToken(rawToken: str) -> str:
    return hashlib.sha256(rawToken.encode("utf-8")).hexdigest()


def refreshTokenExpiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=refreshTokenExpireDays)
