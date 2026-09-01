# Controllers/VariantController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Product import Size, Color, ProductVariant, Product
from Schemas.Variant import (
    SizeCreate, SizeUpdate,
    ColorCreate, ColorUpdate,
    ProductVariantCreate, ProductVariantUpdate,
)
from Services.VariantService import SizeService, ColorService, ProductVariantService

sizeService = SizeService()
colorService = ColorService()
productVariantService = ProductVariantService()


class SizeController:

    def getOrFail(self, db: Session, sizeId: int) -> Size:
        size = sizeService.getById(db, sizeId)
        if size is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Talla con id {sizeId} no encontrada")
        return size

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        return sizeService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, sizeId: int) -> Size:
        return self.getOrFail(db, sizeId)

    def create(self, db: Session, sizeIn: SizeCreate) -> Size:
        return sizeService.create(db, sizeIn)

    def update(self, db: Session, sizeId: int, changes: SizeUpdate) -> Size:
        size = self.getOrFail(db, sizeId)
        return sizeService.update(db, size, changes)

    def delete(self, db: Session, sizeId: int) -> None:
        size = self.getOrFail(db, sizeId)
        sizeService.delete(db, size)


class ColorController:

    def getOrFail(self, db: Session, colorId: int) -> Color:
        color = colorService.getById(db, colorId)
        if color is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Color con id {colorId} no encontrado")
        return color

    def list(self, db: Session, skip: int = 0, limit: int = 50):
        return colorService.list(db, skip=skip, limit=limit)

    def get(self, db: Session, colorId: int) -> Color:
        return self.getOrFail(db, colorId)

    def create(self, db: Session, colorIn: ColorCreate) -> Color:
        return colorService.create(db, colorIn)

    def update(self, db: Session, colorId: int, changes: ColorUpdate) -> Color:
        color = self.getOrFail(db, colorId)
        return colorService.update(db, color, changes)

    def delete(self, db: Session, colorId: int) -> None:
        color = self.getOrFail(db, colorId)
        colorService.delete(db, color)


class ProductVariantController:

    def getOrFail(self, db: Session, productVariantId: int) -> ProductVariant:
        variant = productVariantService.getById(db, productVariantId)
        if variant is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"Variante con id {productVariantId} no encontrada"
            )
        return variant

    def _validateRefs(self, db: Session, productId: int, sizeId: int, colorId: int) -> None:
        if db.get(Product, productId) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Producto con id {productId} no encontrado")
        if db.get(Size, sizeId) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Talla con id {sizeId} no encontrada")
        if db.get(Color, colorId) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Color con id {colorId} no encontrado")

    def listByProduct(self, db: Session, productId: int, skip: int = 0, limit: int = 50):
        return productVariantService.listByProduct(db, productId, skip=skip, limit=limit)

    def get(self, db: Session, productVariantId: int) -> ProductVariant:
        return self.getOrFail(db, productVariantId)

    def create(self, db: Session, variantIn: ProductVariantCreate) -> ProductVariant:
        self._validateRefs(db, variantIn.productId, variantIn.sizeId, variantIn.colorId)
        return productVariantService.create(db, variantIn)

    def update(self, db: Session, productVariantId: int, changes: ProductVariantUpdate) -> ProductVariant:
        variant = self.getOrFail(db, productVariantId)
        if changes.sizeId is not None and db.get(Size, changes.sizeId) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Talla con id {changes.sizeId} no encontrada")
        if changes.colorId is not None and db.get(Color, changes.colorId) is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Color con id {changes.colorId} no encontrado")
        return productVariantService.update(db, variant, changes)

    def delete(self, db: Session, productVariantId: int) -> None:
        variant = self.getOrFail(db, productVariantId)
        productVariantService.delete(db, variant)
