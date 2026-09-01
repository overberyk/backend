# Routes/PaymentRoutes.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Config import getDb
from Controllers.PaymentController import PaymentController
from Controllers.UserController import UserController
from Schemas.Payment import PaymentCreate, PaymentOut, PaymentConfirm
from Security import verifyOwnerOrAdmin, requireRoles
from Models.User import User

PaymentRoutes = APIRouter(prefix="/users/{userId}/orders/{orderId}/payment", tags=["Payment"])
paymentController = PaymentController()
userController = UserController()


@PaymentRoutes.get("/", response_model=PaymentOut)
def get(
    userId: int,
    orderId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return paymentController.get(db, userId, orderId)


@PaymentRoutes.post("/", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create(
    userId: int,
    orderId: int,
    paymentIn: PaymentCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return paymentController.create(db, userId, orderId, paymentIn)


@PaymentRoutes.patch("/confirm", response_model=PaymentOut)
def confirm(
    userId: int,
    orderId: int,
    changes: PaymentConfirm,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin")),
):
    userController.getOrFail(db, userId)
    return paymentController.confirm(db, userId, orderId, changes)
