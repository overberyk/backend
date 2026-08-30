# Services/ProductService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Product import Product
from Schemas.Product import ProductCreate, ProductUpdate


class ProductService:

    def getById(self, db: Session, productId: int) -> Optional[Product]:
        return db.get(Product, productId)

    def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        categoryId: Optional[int] = None,
        brandId: Optional[int] = None,
        typeId: Optional[int] = None,
    ) -> List[Product]:
        stmt = select(Product)
        if categoryId is not None:
            stmt = stmt.where(Product.categoryId == categoryId)
        if brandId is not None:
            stmt = stmt.where(Product.brandId == brandId)
        if typeId is not None:
            stmt = stmt.where(Product.typeId == typeId)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, productIn: ProductCreate) -> Product:
        newProduct = Product(**productIn.model_dump())
        db.add(newProduct)
        db.commit()
        db.refresh(newProduct)
        return newProduct

    def update(self, db: Session, product: Product, changes: ProductUpdate) -> Product:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()
