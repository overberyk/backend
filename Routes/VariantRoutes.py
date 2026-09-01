# Routes/VariantRoutes.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.VariantController import SizeController, ColorController, ProductVariantController
from Schemas.Variant import (
    SizeCreate, SizeOut, SizeUpdate,
    ColorCreate, ColorOut, ColorUpdate,
    ProductVariantCreate, ProductVariantOut, ProductVariantUpdate,
)
from Security import requireRoles
from Models.User import User

VariantRoutes = APIRouter(tags=["Variants"])
sizeController = SizeController()
colorController = ColorController()
productVariantController = ProductVariantController()


# ---------------------- Sizes ----------------------

@VariantRoutes.get("/sizes/", response_model=List[SizeOut])
def listSizes(skip: int = 0, limit: int = 50, db: Session = Depends(getDb)):
    return sizeController.list(db, skip=skip, limit=limit)


@VariantRoutes.get("/sizes/{sizeId}", response_model=SizeOut)
def getSize(sizeId: int, db: Session = Depends(getDb)):
    return sizeController.get(db, sizeId)


@VariantRoutes.post("/sizes/", response_model=SizeOut, status_code=status.HTTP_201_CREATED)
def createSize(
    sizeIn: SizeCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return sizeController.create(db, sizeIn)


@VariantRoutes.patch("/sizes/{sizeId}", response_model=SizeOut)
def updateSize(
    sizeId: int,
    changes: SizeUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return sizeController.update(db, sizeId, changes)


@VariantRoutes.delete("/sizes/{sizeId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteSize(
    sizeId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    sizeController.delete(db, sizeId)


# ---------------------- Colors ----------------------

@VariantRoutes.get("/colors/", response_model=List[ColorOut])
def listColors(skip: int = 0, limit: int = 50, db: Session = Depends(getDb)):
    return colorController.list(db, skip=skip, limit=limit)


@VariantRoutes.get("/colors/{colorId}", response_model=ColorOut)
def getColor(colorId: int, db: Session = Depends(getDb)):
    return colorController.get(db, colorId)


@VariantRoutes.post("/colors/", response_model=ColorOut, status_code=status.HTTP_201_CREATED)
def createColor(
    colorIn: ColorCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return colorController.create(db, colorIn)


@VariantRoutes.patch("/colors/{colorId}", response_model=ColorOut)
def updateColor(
    colorId: int,
    changes: ColorUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return colorController.update(db, colorId, changes)


@VariantRoutes.delete("/colors/{colorId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteColor(
    colorId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    colorController.delete(db, colorId)


# ---------------------- Product Variants ----------------------

@VariantRoutes.get("/products/{productId}/variants", response_model=List[ProductVariantOut])
def listVariantsByProduct(productId: int, skip: int = 0, limit: int = 50, db: Session = Depends(getDb)):
    return productVariantController.listByProduct(db, productId, skip=skip, limit=limit)


@VariantRoutes.get("/product-variants/{productVariantId}", response_model=ProductVariantOut)
def getVariant(productVariantId: int, db: Session = Depends(getDb)):
    return productVariantController.get(db, productVariantId)


@VariantRoutes.post(
    "/product-variants/", response_model=ProductVariantOut, status_code=status.HTTP_201_CREATED
)
def createVariant(
    variantIn: ProductVariantCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return productVariantController.create(db, variantIn)


@VariantRoutes.patch("/product-variants/{productVariantId}", response_model=ProductVariantOut)
def updateVariant(
    productVariantId: int,
    changes: ProductVariantUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return productVariantController.update(db, productVariantId, changes)


@VariantRoutes.delete("/product-variants/{productVariantId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteVariant(
    productVariantId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    productVariantController.delete(db, productVariantId)
