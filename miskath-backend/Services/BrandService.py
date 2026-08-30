# Services/BrandService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Product import Brand
from Schemas.Brand import BrandCreate, BrandUpdate


class BrandService:

    def list(self, db: Session, skip: int = 0, limit: int = 50) -> List[Brand]:
        stmt = select(Brand).offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def getById(self, db: Session, brandId: int) -> Optional[Brand]:
        return db.get(Brand, brandId)

    def create(self, db: Session, brandIn: BrandCreate) -> Brand:
        newBrand = Brand(**brandIn.model_dump())
        db.add(newBrand)
        db.commit()
        db.refresh(newBrand)
        return newBrand

    def update(self, db: Session, brand: Brand, changes: BrandUpdate) -> Brand:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(brand, field, value)
        db.commit()
        db.refresh(brand)
        return brand

    def delete(self, db: Session, brand: Brand) -> None:
        db.delete(brand)
        db.commit()
