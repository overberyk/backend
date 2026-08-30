# Security.py
"""
Dependencias de FastAPI para autenticación y autorización de rutas.
No está contemplado en el estándar del PDF (es específico de FastAPI,
Flask no maneja dependencias inyectadas de la misma forma), pero es
necesario para proteger los endpoints con JWT y roles.
"""

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from Config import getDb, decodeAccessToken
from Models.User import User


oauth2Scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def getCurrentUser(
    token: str = Depends(oauth2Scheme), db: Session = Depends(getDb)
) -> User:
    invalidCredentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decodeAccessToken(token)
    if payload is None:
        raise invalidCredentials

    userId = payload.get("sub")
    if userId is None:
        raise invalidCredentials

    user = db.get(User, int(userId))
    if user is None:
        raise invalidCredentials

    return user


def requireRoles(*allowedRoles: str) -> Callable:
    def _checkRole(currentUser: User = Depends(getCurrentUser)) -> User:
        if currentUser.role.name not in allowedRoles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"No tienes permiso para esta acción "
                    f"(rol requerido: {', '.join(allowedRoles)})"
                ),
            )
        return currentUser

    return _checkRole


def verifyOwnerOrAdmin(userId: int, currentUser: User = Depends(getCurrentUser)) -> User:
    isOwner = currentUser.userId == userId
    isAdmin = currentUser.role.name == "admin"
    if not (isOwner or isAdmin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a los datos de otro usuario",
        )
    return currentUser
