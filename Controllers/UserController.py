# Controllers/UserController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.User import User
from Schemas.User import UserCreate, UserUpdate, UserChangeRole
from Services.UserService import UserService

userService = UserService()


class UserController:

    def getOrFail(self, db: Session, userId: int) -> User:
        user = userService.getById(db, userId)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con id {userId} no encontrado",
            )
        return user

    def list(self, db: Session, skip: int = 0, limit: int = 20):
        return userService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, userId: int) -> User:
        return self.getOrFail(db, userId)

    def create(self, db: Session, userIn: UserCreate) -> User:
        existing = userService.getByEmail(db, userIn.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario registrado con ese correo",
            )
        return userService.create(db, userIn)

    def update(self, db: Session, userId: int, changes: UserUpdate) -> User:
        user = self.getOrFail(db, userId)
        return userService.update(db, user, changes)

    def delete(self, db: Session, userId: int) -> None:
        user = self.getOrFail(db, userId)
        userService.delete(db, user)

    def changeRole(self, db: Session, userId: int, change: UserChangeRole) -> User:
        user = self.getOrFail(db, userId)
        try:
            return userService.changeRole(db, user, change.roleId)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
