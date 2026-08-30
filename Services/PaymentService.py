# Services/PaymentService.py
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Payment import Payment, PaymentStatus
from Models.Order import Order, OrderStatus
from Schemas.Payment import PaymentCreate


class OrderAlreadyPaidError(Exception):
    pass


class InvalidPaymentStatusError(Exception):
    pass


class PaymentService:

    def getById(self, db: Session, paymentId: int) -> Optional[Payment]:
        return db.get(Payment, paymentId)

    def getByOrder(self, db: Session, orderId: int) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.orderId == orderId)
        return db.scalars(stmt).first()

    def _getPaymentStatusByName(self, db: Session, name: str) -> PaymentStatus:
        stmt = select(PaymentStatus).where(PaymentStatus.name == name)
        status = db.scalars(stmt).first()
        if status is None:
            raise RuntimeError(
                f"The PaymentStatus '{name}' doesn't exist in the database. "
                f"Create it first (payment_status seed)."
            )
        return status

    def _getOrderStatusByName(self, db: Session, name: str) -> OrderStatus:
        stmt = select(OrderStatus).where(OrderStatus.name == name)
        status = db.scalars(stmt).first()
        if status is None:
            raise RuntimeError(
                f"The OrderStatus '{name}' doesn't exist in the database. "
                f"Create it first (order_status seed)."
            )
        return status

    def createForOrder(self, db: Session, order: Order, paymentIn: PaymentCreate) -> Payment:
        existing = self.getByOrder(db, order.orderId)
        if existing is not None and existing.paymentStatus.name == "Approved":
            raise OrderAlreadyPaidError(
                f"Order {order.orderId} already has an approved payment"
            )

        total: Decimal = sum(
            (d.price * d.quantity for d in order.orderDetail),
            start=Decimal("0"),
        )
        initStatus = self._getPaymentStatusByName(db, "Pending")

        newPayment = Payment(
            orderId=order.orderId,
            paymentMethodId=paymentIn.paymentMethodId,
            paymentStatusId=initStatus.paymentStatusId,
            total=total,
        )
        db.add(newPayment)
        db.commit()
        db.refresh(newPayment)
        return newPayment

    def confirm(self, db: Session, payment: Payment, paymentStatusId: int) -> Payment:
        newStatus = db.get(PaymentStatus, paymentStatusId)
        if newStatus is None:
            raise InvalidPaymentStatusError(f"No PaymentStatus exists with id {paymentStatusId}")

        payment.paymentStatusId = paymentStatusId

        if newStatus.name == "Approved":
            inProcess = self._getOrderStatusByName(db, "In process")
            payment.order.orderStatusId = inProcess.orderStatusId

        db.commit()
        db.refresh(payment)
        return payment
