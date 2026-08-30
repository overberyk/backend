# Models/Cart.py
from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models.Base import Base, generateUuid, TimestampMixin


class Cart(Base, TimestampMixin):
    __tablename__ = "cart"

    cartId: Mapped[int] = mapped_column("cart_id", primary_key=True, autoincrement=True)
    cartUuid: Mapped[str] = mapped_column("cart_uuid", String(45), unique=True, default=generateUuid)

    userId: Mapped[int] = mapped_column("user_id", ForeignKey("user.user_id"))

    user: Mapped["User"] = relationship(back_populates="carts")
    details: Mapped[List["CartDetail"]] = relationship(
        back_populates="cart", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<cart_id={self.cartId} user_id={self.userId}>"


class CartDetail(Base):
    __tablename__ = "cart_detail"

    cartDetailId: Mapped[int] = mapped_column("cart_detail_id", primary_key=True, autoincrement=True)
    cartDetailUuid: Mapped[str] = mapped_column("cart_detail_uuid", String(45), unique=True, default=generateUuid)
    quantity: Mapped[int] = mapped_column()
    unitPrice: Mapped[Decimal] = mapped_column("unit_price", Numeric(10, 2))

    cartId: Mapped[int] = mapped_column("cart_id", ForeignKey("cart.cart_id"))
    productVariantId: Mapped[int] = mapped_column(
        "product_variant_id", ForeignKey("product_variant.product_variant_id")
    )

    cart: Mapped["Cart"] = relationship(back_populates="details")
    productVariant: Mapped["ProductVariant"] = relationship(back_populates="cartDetails")

    def __repr__(self) -> str:
        return f"<DetalleCarrito id={self.cartDetailId} cantidad={self.quantity}>"
