# Controllers/ProductController.py
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Product import Product
from Schemas.Product import ProductCreate, ProductUpdate
from Services.ProductService import ProductService

productService = ProductService()


class ProductController:

    def getOrFail(self, db: Session, productId: int) -> Product:
        product = productService.getById(db, productId)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {productId} no encontrado",
            )
        return product

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        categoryId: Optional[int] = None,
        brandId: Optional[int] = None,
        typeId: Optional[int] = None,
    ):
        return productService.list(
            db, skip=skip, limit=limit,
            categoryId=categoryId, brandId=brandId, typeId=typeId,
        )

    def get(self, db: Session, productId: int) -> Product:
        return self.getOrFail(db, productId)

    def create(self, db: Session, productIn: ProductCreate) -> Product:
        return productService.create(db, productIn)

    def update(self, db: Session, productId: int, changes: ProductUpdate) -> Product:
        product = self.getOrFail(db, productId)
        return productService.update(db, product, changes)

    def delete(self, db: Session, productId: int) -> None:
        product = self.getOrFail(db, productId)
        productService.delete(db, product)
