# Models/Payment.py
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models.Base import Base, generateUuid, TimestampMixin


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    paymentMethodId: Mapped[int] = mapped_column("payment_method_id", primary_key=True, autoincrement=True)
    paymentMethodUuid: Mapped[str] = mapped_column(
        "payment_method_uuid", String(45), unique=True, default=generateUuid
    )
    name: Mapped[str] = mapped_column(String(45))

    payments: Mapped[List["Payment"]] = relationship(back_populates="paymentMethod")

    def __repr__(self) -> str:
        return f"<MetodoPago id={self.paymentMethodId} nombre={self.name!r}>"


class PaymentStatus(Base):
    __tablename__ = "payment_status"

    paymentStatusId: Mapped[int] = mapped_column("payment_status_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45))

    payments: Mapped[List["Payment"]] = relationship(back_populates="paymentStatus")

    def __repr__(self) -> str:
        return f"<EstadoPago id={self.paymentStatusId} nombre={self.name!r}>"


class Payment(Base, TimestampMixin):
    __tablename__ = "payment"

    paymentId: Mapped[int] = mapped_column("payment_id", primary_key=True, autoincrement=True)
    paymentUuid: Mapped[str] = mapped_column("payment_uuid", String(45), unique=True, default=generateUuid)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    paymentMethodId: Mapped[int] = mapped_column("payment_method_id", ForeignKey("payment_method.payment_method_id"))
    paymentStatusId: Mapped[int] = mapped_column("payment_status_id", ForeignKey("payment_status.payment_status_id"))
    orderId: Mapped[Optional[int]] = mapped_column("order_id", ForeignKey("order.order_id"))

    paymentMethod: Mapped["PaymentMethod"] = relationship(back_populates="payments")
    paymentStatus: Mapped["PaymentStatus"] = relationship(back_populates="payments")
    order: Mapped[Optional["Order"]] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return f"<Pago id={self.paymentId} total={self.total}>"
