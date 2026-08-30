# Routes/CartRoutes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.CartController import CartController
from Schemas.Cart import CartOut
from Schemas.CartDetail import CartDetailCreate, CartDetailOut, CartDetailUpdate
from Security import verifyOwnerOrAdmin
from Models.User import User

CartRoutes = APIRouter(prefix="/users/{userId}/cart", tags=["Cart"])
cartController = CartController()


@CartRoutes.get("/", response_model=CartOut)
def get(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return cartController.get(db, userId)


@CartRoutes.post("/details", response_model=CartDetailOut, status_code=status.HTTP_201_CREATED)
def addItem(
    userId: int,
    itemIn: CartDetailCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return cartController.addItem(db, userId, itemIn)


@CartRoutes.patch("/details/{detailId}", response_model=CartDetailOut)
def updateItem(
    userId: int,
    detailId: int,
    changes: CartDetailUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return cartController.updateItem(db, userId, detailId, changes)


@CartRoutes.delete("/details/{detailId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteItem(
    userId: int,
    detailId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    cartController.deleteItem(db, userId, detailId)


@CartRoutes.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def empty(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    cartController.empty(db, userId)
