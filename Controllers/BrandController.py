# Controllers/BrandController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Product import Brand
from Schemas.Brand import BrandCreate, BrandUpdate
from Services.BrandService import BrandService

brandService = BrandService()


class BrandController:

    def getOrFail(self, db: Session, brandId: int) -> Brand:
        brand = brandService.getById(db, brandId)
        if brand is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Marca con id {brandId} no encontrada",
            )
        return brand

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        return brandService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, brandId: int) -> Brand:
        return self.getOrFail(db, brandId)

    def create(self, db: Session, brandIn: BrandCreate) -> Brand:
        return brandService.create(db, brandIn)

    def update(self, db: Session, brandId: int, changes: BrandUpdate) -> Brand:
        brand = self.getOrFail(db, brandId)
        return brandService.update(db, brand, changes)

    def delete(self, db: Session, brandId: int) -> None:
        brand = self.getOrFail(db, brandId)
        brandService.delete(db, brand)
