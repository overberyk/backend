# Services/CategoryService.py
# FIX: en el original había dos métodos "get" (uno por id, otro de listado)
# con el mismo nombre en Python, y el segundo pisaba al primero. Aquí se
# separan como getById() y list(), siguiendo la convención del PDF.
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Product import Category
from Schemas.Category import CategoryCreate, CategoryUpdate


class CategoryService:

    def list(self, db: Session, skip: int = 0, limit: int = 20) -> List[Category]:
        stmt = select(Category).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, categoryId: int) -> Optional[Category]:
        return db.get(Category, categoryId)

    def create(self, db: Session, categoryIn: CategoryCreate) -> Category:
        newCategory = Category(**categoryIn.model_dump())
        db.add(newCategory)
        db.commit()
        db.refresh(newCategory)
        return newCategory

    def update(self, db: Session, category: Category, changes: CategoryUpdate) -> Category:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(category, field, value)
        db.commit()
        db.refresh(category)
        return category

    def delete(self, db: Session, category: Category) -> None:
        db.delete(category)
        db.commit()
