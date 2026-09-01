# Routes/BrandRoutes.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.BrandController import BrandController
from Schemas.Brand import BrandCreate, BrandOut, BrandUpdate
from Security import requireRoles
from Models.User import User

BrandRoutes = APIRouter(prefix="/brands", tags=["Brands"])
brandController = BrandController()


@BrandRoutes.get("/", response_model=List[BrandOut])
def list(skip: int = 0, limit: int = 50, db: Session = Depends(getDb)):
    return brandController.list(db, skip=skip, limit=limit)


@BrandRoutes.get("/{brandId}", response_model=BrandOut)
def get(brandId: int, db: Session = Depends(getDb)):
    return brandController.get(db, brandId)


@BrandRoutes.post("/", response_model=BrandOut, status_code=status.HTTP_201_CREATED)
def create(
    brandIn: BrandCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return brandController.create(db, brandIn)


@BrandRoutes.patch("/{brandId}", response_model=BrandOut)
def update(
    brandId: int,
    changes: BrandUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    return brandController.update(db, brandId, changes)


@BrandRoutes.delete("/{brandId}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    brandId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin", "seller")),
):
    brandController.delete(db, brandId)
