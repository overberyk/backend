# Controllers/TypeController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Product import Type
from Schemas.Type import TypeCreate, TypeUpdate
from Services.TypeService import TypeService

typeService = TypeService()


class TypeController:

    def getOrFail(self, db: Session, typeId: int) -> Type:
        typeObj = typeService.getById(db, typeId)
        if typeObj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tipo con id {typeId} no encontrado",
            )
        return typeObj

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        return typeService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, typeId: int) -> Type:
        return self.getOrFail(db, typeId)

    def create(self, db: Session, typeIn: TypeCreate) -> Type:
        return typeService.create(db, typeIn)

    def update(self, db: Session, typeId: int, changes: TypeUpdate) -> Type:
        typeObj = self.getOrFail(db, typeId)
        return typeService.update(db, typeObj, changes)

    def delete(self, db: Session, typeId: int) -> None:
        typeObj = self.getOrFail(db, typeId)
        typeService.delete(db, typeObj)
