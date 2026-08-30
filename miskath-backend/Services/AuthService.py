# Services/AuthService.py
"""
Operaciones de refresh tokens: emisión, validación, rotación (usar uno lo
invalida y crea uno nuevo) y revocación (logout).
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.User import RefreshToken, User
from Config import generateRefreshToken, hashRefreshToken, refreshTokenExpiry


class InvalidRefreshTokenError(Exception):
    pass


class AuthService:

    def issueRefreshToken(self, db: Session, user: User) -> str:
        rawToken = generateRefreshToken()
        record = RefreshToken(
            tokenHash=hashRefreshToken(rawToken),
            userId=user.userId,
            expiresAt=refreshTokenExpiry(),
        )
        db.add(record)
        db.commit()
        return rawToken

    def _getValidTokenRecord(self, db: Session, rawToken: str) -> Optional[RefreshToken]:
        tokenHash = hashRefreshToken(rawToken)
        stmt = select(RefreshToken).where(RefreshToken.tokenHash == tokenHash)
        record = db.scalars(stmt).first()

        if record is None or record.revoked:
            return None

        expiresAt = record.expiresAt
        if expiresAt.tzinfo is None:
            expiresAt = expiresAt.replace(tzinfo=timezone.utc)
        if expiresAt < datetime.now(timezone.utc):
            return None

        return record

    def rotateRefreshToken(self, db: Session, rawToken: str) -> tuple[User, str]:
        record = self._getValidTokenRecord(db, rawToken)
        if record is None:
            raise InvalidRefreshTokenError("Refresh token inválido, expirado o revocado")

        user = db.get(User, record.userId)
        if user is None:
            raise InvalidRefreshTokenError("El usuario asociado a este token ya no existe")

        record.revoked = True
        db.add(record)
        db.commit()

        newRawToken = self.issueRefreshToken(db, user)
        return user, newRawToken

    def revokeRefreshToken(self, db: Session, rawToken: str) -> None:
        tokenHash = hashRefreshToken(rawToken)
        stmt = select(RefreshToken).where(RefreshToken.tokenHash == tokenHash)
        record = db.scalars(stmt).first()
        if record is not None and not record.revoked:
            record.revoked = True
            db.add(record)
            db.commit()

    def revokeAllRefreshTokensForUser(self, db: Session, userId: int) -> None:
        stmt = select(RefreshToken).where(
            RefreshToken.userId == userId, RefreshToken.revoked.is_(False)
        )
        records = db.scalars(stmt).all()
        for record in records:
            record.revoked = True
            db.add(record)
        db.commit()
