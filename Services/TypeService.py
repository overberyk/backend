# Services/TypeService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Product import Type
from Schemas.Type import TypeCreate, TypeUpdate


class TypeService:

    def list(self, db: Session, skip: int = 0, limit: int = 20) -> List[Type]:
        stmt = select(Type).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, typeId: int) -> Optional[Type]:
        return db.get(Type, typeId)

    def create(self, db: Session, typeIn: TypeCreate) -> Type:
        newType = Type(**typeIn.model_dump())
        db.add(newType)
        db.commit()
        db.refresh(newType)
        return newType

    def update(self, db: Session, typeObj: Type, changes: TypeUpdate) -> Type:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(typeObj, field, value)
        db.commit()
        db.refresh(typeObj)
        return typeObj

    def delete(self, db: Session, typeObj: Type) -> None:
        db.delete(typeObj)
        db.commit()
