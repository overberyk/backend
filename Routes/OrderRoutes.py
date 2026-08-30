# Routes/OrderRoutes.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.OrderController import OrderController
from Controllers.UserController import UserController
from Schemas.Order import OrderOut
from Security import verifyOwnerOrAdmin
from Models.User import User

OrderRoutes = APIRouter(prefix="/users/{userId}/orders", tags=["Orders"])
orderController = OrderController()
userController = UserController()


@OrderRoutes.get("/", response_model=List[OrderOut])
def list(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return orderController.list(db, userId)


@OrderRoutes.get("/{orderId}", response_model=OrderOut)
def get(
    userId: int,
    orderId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return orderController.get(db, userId, orderId)


@OrderRoutes.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return orderController.create(db, userId)
