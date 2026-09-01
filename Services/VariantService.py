# Services/VariantService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Product import Size, Color, ProductVariant
from Schemas.Variant import (
    SizeCreate, SizeUpdate,
    ColorCreate, ColorUpdate,
    ProductVariantCreate, ProductVariantUpdate,
)


class SizeService:

    def list(self, db: Session, skip: int = 0, limit: int = 50) -> List[Size]:
        stmt = select(Size).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, sizeId: int) -> Optional[Size]:
        return db.get(Size, sizeId)

    def create(self, db: Session, sizeIn: SizeCreate) -> Size:
        newSize = Size(**sizeIn.model_dump())
        db.add(newSize)
        db.commit()
        db.refresh(newSize)
        return newSize

    def update(self, db: Session, size: Size, changes: SizeUpdate) -> Size:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(size, field, value)
        db.commit()
        db.refresh(size)
        return size

    def delete(self, db: Session, size: Size) -> None:
        db.delete(size)
        db.commit()


class ColorService:

    def list(self, db: Session, skip: int = 0, limit: int = 50) -> List[Color]:
        stmt = select(Color).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, colorId: int) -> Optional[Color]:
        return db.get(Color, colorId)

    def create(self, db: Session, colorIn: ColorCreate) -> Color:
        newColor = Color(**colorIn.model_dump())
        db.add(newColor)
        db.commit()
        db.refresh(newColor)
        return newColor

    def update(self, db: Session, color: Color, changes: ColorUpdate) -> Color:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(color, field, value)
        db.commit()
        db.refresh(color)
        return color

    def delete(self, db: Session, color: Color) -> None:
        db.delete(color)
        db.commit()


class ProductVariantService:

    def listByProduct(self, db: Session, productId: int, skip: int = 0, limit: int = 50) -> List[ProductVariant]:
        stmt = (
            select(ProductVariant)
            .where(ProductVariant.productId == productId)
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, productVariantId: int) -> Optional[ProductVariant]:
        return db.get(ProductVariant, productVariantId)

    def create(self, db: Session, variantIn: ProductVariantCreate) -> ProductVariant:
        newVariant = ProductVariant(**variantIn.model_dump())
        db.add(newVariant)
        db.commit()
        db.refresh(newVariant)
        return newVariant

    def update(self, db: Session, variant: ProductVariant, changes: ProductVariantUpdate) -> ProductVariant:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(variant, field, value)
        db.commit()
        db.refresh(variant)
        return variant

    def delete(self, db: Session, variant: ProductVariant) -> None:
        db.delete(variant)
        db.commit()
