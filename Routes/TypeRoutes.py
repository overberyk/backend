# Routes/TypeRoutes.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.TypeController import TypeController
from Schemas.Type import TypeCreate, TypeOut, TypeUpdate
from Security import requireRoles
from Models.User import User

TypeRoutes = APIRouter(prefix="/types", tags=["Types"])
typeController = TypeController()


@TypeRoutes.get("/", response_model=List[TypeOut])
def list(skip: int = 0, limit: int = 50, db: Session = Depends(getDb)):
    return typeController.list(db, skip=skip, limit=limit)


@TypeRoutes.get("/{typeId}", response_model=TypeOut)
def get(typeId: int, db: Session = Depends(getDb)):
    return typeController.get(db, typeId)


@TypeRoutes.post("/", response_model=TypeOut, status_code=status.HTTP_201_CREATED)
def create(
    typeIn: TypeCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return typeController.create(db, typeIn)


@TypeRoutes.patch("/{typeId}", response_model=TypeOut)
def update(
    typeId: int,
    changes: TypeUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return typeController.update(db, typeId, changes)


@TypeRoutes.delete("/{typeId}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    typeId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    typeController.delete(db, typeId)
