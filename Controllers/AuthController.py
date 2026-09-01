# Controllers/AuthController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Schemas.Auth import Token, RefreshRequest, LogoutRequest
from Services.AuthService import AuthService, InvalidRefreshTokenError
from Services.UserService import UserService
from Config import createAccessToken, verifyPassword

authService = AuthService()
userService = UserService()


class AuthController:

    def login(self, db: Session, email: str, password: str) -> Token:
        invalidCredentials = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = userService.getByEmail(db, email)
        if user is None:
            raise invalidCredentials

        if not verifyPassword(password, user.passwordHash):
            raise invalidCredentials

        accessToken = createAccessToken(data={"sub": str(user.userId)})
        refreshToken = authService.issueRefreshToken(db, user)
        return Token(accessToken=accessToken, refreshToken=refreshToken)

    def refresh(self, db: Session, payload: RefreshRequest) -> Token:
        """Rota un refresh token válido por un nuevo par access/refresh. El
        token recibido se revoca de inmediato (rotación): si alguien más lo
        reutiliza después, va a fallar."""
        try:
            user, newRefreshToken = authService.rotateRefreshToken(db, payload.refreshToken)
        except InvalidRefreshTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido, expirado o revocado. Vuelve a iniciar sesión.",
            )

        accessToken = createAccessToken(data={"sub": str(user.userId)})
        return Token(accessToken=accessToken, refreshToken=newRefreshToken)

    def logout(self, db: Session, payload: LogoutRequest) -> None:
        authService.revokeRefreshToken(db, payload.refreshToken)
