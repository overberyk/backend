# Models/Order.py
from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models.Base import Base, generateUuid, TimestampMixin


class OrderStatus(Base):
    __tablename__ = "order_status"

    orderStatusId: Mapped[int] = mapped_column("order_status_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45))

    orders: Mapped[List["Order"]] = relationship(back_populates="orderStatus")

    def __repr__(self) -> str:
        return f"<order_status_id={self.orderStatusId} name={self.name!r}>"


class Order(Base, TimestampMixin):
    __tablename__ = "order"

    orderId: Mapped[int] = mapped_column("order_id", primary_key=True, autoincrement=True)
    orderUuid: Mapped[str] = mapped_column("order_uuid", String(45), unique=True, default=generateUuid)

    userId: Mapped[int] = mapped_column("user_id", ForeignKey("user.user_id"))
    addressId: Mapped[int] = mapped_column("address_id", ForeignKey("address.address_id"))
    orderStatusId: Mapped[int] = mapped_column("order_status_id", ForeignKey("order_status.order_status_id"))

    user: Mapped["User"] = relationship(back_populates="orders")
    address: Mapped["Address"] = relationship(back_populates="orders")
    orderStatus: Mapped["OrderStatus"] = relationship(back_populates="orders")
    payments: Mapped[List["Payment"]] = relationship(back_populates="order")
    orderDetail: Mapped[List["OrderDetail"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Pedido id={self.orderId}>"


class OrderDetail(Base):
    __tablename__ = "order_detail"

    orderDetailId: Mapped[int] = mapped_column("order_detail_id", primary_key=True, autoincrement=True)
    orderDetailUuid: Mapped[str] = mapped_column("order_detail_uuid", String(45), unique=True, default=generateUuid)
    quantity: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    orderId: Mapped[int] = mapped_column("order_id", ForeignKey("order.order_id"))
    productVariantId: Mapped[int] = mapped_column(
        "product_variant_id", ForeignKey("product_variant.product_variant_id")
    )

    order: Mapped["Order"] = relationship(back_populates="orderDetail")
    productVariant: Mapped["ProductVariant"] = relationship(back_populates="orderDetails")

    def __repr__(self) -> str:
        return f"<DetallePedido id={self.orderDetailId} cantidad={self.quantity}>"
