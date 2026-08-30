# Controllers/CategoryController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Product import Category
from Schemas.Category import CategoryCreate, CategoryUpdate
from Services.CategoryService import CategoryService

categoryService = CategoryService()


class CategoryController:

    def getOrFail(self, db: Session, categoryId: int) -> Category:
        category = categoryService.getById(db, categoryId)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoría con id {categoryId} no encontrada",
            )
        return category

    def list(self, db: Session, skip: int = 0, limit: int = 20):
        return categoryService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, categoryId: int) -> Category:
        return self.getOrFail(db, categoryId)

    def create(self, db: Session, categoryIn: CategoryCreate) -> Category:
        return categoryService.create(db, categoryIn)

    def update(self, db: Session, categoryId: int, changes: CategoryUpdate) -> Category:
        category = self.getOrFail(db, categoryId)
        return categoryService.update(db, category, changes)

    def delete(self, db: Session, categoryId: int) -> None:
        category = self.getOrFail(db, categoryId)
        categoryService.delete(db, category)
