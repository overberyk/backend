# Controllers/PaymentController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Payment import Payment
from Schemas.Payment import PaymentCreate, PaymentConfirm
from Controllers.OrderController import OrderController
from Services.PaymentService import (
    PaymentService, OrderAlreadyPaidError, InvalidPaymentStatusError,
)

paymentService = PaymentService()
orderController = OrderController()


class PaymentController:

    def get(self, db: Session, userId: int, orderId: int) -> Payment:
        orderController.getOrFail(db, userId, orderId)
        payment = paymentService.getByOrder(db, orderId)
        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Este pedido todavía no tiene un pago asociado",
            )
        return payment

    def create(self, db: Session, userId: int, orderId: int, paymentIn: PaymentCreate) -> Payment:
        order = orderController.getOrFail(db, userId, orderId)
        try:
            return paymentService.createForOrder(db, order, paymentIn)
        except OrderAlreadyPaidError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    def confirm(self, db: Session, userId: int, orderId: int, changes: PaymentConfirm) -> Payment:
        orderController.getOrFail(db, userId, orderId)
        payment = paymentService.getByOrder(db, orderId)
        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Este pedido todavía no tiene un pago asociado",
            )
        try:
            return paymentService.confirm(db, payment, changes.paymentStatusId)
        except InvalidPaymentStatusError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
