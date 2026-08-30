# Routes/CategoryRoutes.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.CategoryController import CategoryController
from Schemas.Category import CategoryCreate, CategoryOut, CategoryUpdate
from Security import requireRoles
from Models.User import User

CategoryRoutes = APIRouter(prefix="/categories", tags=["Categories"])
categoryController = CategoryController()


@CategoryRoutes.get("/", response_model=List[CategoryOut])
def list(skip: int = 0, limit: int = 20, db: Session = Depends(getDb)):
    return categoryController.list(db, skip=skip, limit=limit)


@CategoryRoutes.get("/{categoryId}", response_model=CategoryOut)
def get(categoryId: int, db: Session = Depends(getDb)):
    return categoryController.get(db, categoryId)


@CategoryRoutes.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create(
    categoryIn: CategoryCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return categoryController.create(db, categoryIn)


@CategoryRoutes.patch("/{categoryId}", response_model=CategoryOut)
def update(
    categoryId: int,
    changes: CategoryUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return categoryController.update(db, categoryId, changes)


@CategoryRoutes.delete("/{categoryId}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    categoryId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    categoryController.delete(db, categoryId)
