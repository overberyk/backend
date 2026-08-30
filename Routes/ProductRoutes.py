# Routes/ProductRoutes.py
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.ProductController import ProductController
from Schemas.Product import ProductCreate, ProductOut, ProductUpdate
from Security import requireRoles
from Models.User import User

ProductRoutes = APIRouter(prefix="/products", tags=["Products"])
productController = ProductController()


@ProductRoutes.get("/", response_model=List[ProductOut])
def list(
    skip: int = 0,
    limit: int = 20,
    categoryId: Optional[int] = None,
    brandId: Optional[int] = None,
    typeId: Optional[int] = None,
    db: Session = Depends(getDb),
):
    return productController.list(
        db, skip=skip, limit=limit,
        categoryId=categoryId, brandId=brandId, typeId=typeId,
    )


@ProductRoutes.get("/{productId}", response_model=ProductOut)
def get(productId: int, db: Session = Depends(getDb)):
    return productController.get(db, productId)


@ProductRoutes.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create(
    productIn: ProductCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return productController.create(db, productIn)


@ProductRoutes.patch("/{productId}", response_model=ProductOut)
def update(
    productId: int,
    changes: ProductUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return productController.update(db, productId, changes)


@ProductRoutes.delete("/{productId}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    productId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    productController.delete(db, productId)
