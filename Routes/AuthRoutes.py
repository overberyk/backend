# Routes/AuthRoutes.py
from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from Config import getDb, limiter
from Controllers.AuthController import AuthController
from Schemas.Auth import LogoutRequest, RefreshRequest, Token

AuthRoutes = APIRouter(prefix="/auth", tags=["Auth"])
authController = AuthController()


@AuthRoutes.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    formData: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(getDb),
) -> Token:
    return authController.login(db, formData.username, formData.password)


@AuthRoutes.post("/refresh", response_model=Token)
@limiter.limit("20/minute")
def refresh(
    request: Request,
    payload: RefreshRequest,
    db: Session = Depends(getDb),
) -> Token:
    return authController.refresh(db, payload)


@AuthRoutes.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: LogoutRequest, db: Session = Depends(getDb)) -> None:
    authController.logout(db, payload)
