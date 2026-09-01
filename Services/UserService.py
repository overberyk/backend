# Services/UserService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.User import User, Role
from Schemas.User import UserCreate, UserUpdate
from Config import hashPassword


class UserService:

    def getById(self, db: Session, userId: int) -> Optional[User]:
        return db.get(User, userId)

    def getByEmail(self, db: Session, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()

    def list(self, db: Session, skip: int = 0, limit: int = 20) -> List[User]:
        stmt = select(User).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def _getRoleByName(self, db: Session, name: str) -> Role:
        stmt = select(Role).where(Role.name == name)
        role = db.scalars(stmt).first()
        if role is None:
            raise RuntimeError(
                f"The Role '{name}' doesn't exist in the database. Create it first (role seed)."
            )
        return role

    def create(self, db: Session, userIn: UserCreate) -> User:
        clientRole = self._getRoleByName(db, "client")
        data = userIn.model_dump(exclude={"password"})
        newUser = User(
            **data,
            passwordHash=hashPassword(userIn.password),
            roleId=clientRole.roleId,
        )
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser

    def update(self, db: Session, user: User, changes: UserUpdate) -> User:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(user, field, value)
        db.commit()
        db.refresh(user)
        return user

    def changeRole(self, db: Session, user: User, roleId: int) -> User:
        role = db.get(Role, roleId)
        if role is None:
            raise ValueError(f"No Role exists with id {roleId}")
        user.roleId = roleId
        db.commit()
        db.refresh(user)
        return user

    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
