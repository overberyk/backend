# Services/OrderService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Order import Order, OrderDetail, OrderStatus
from Models.User import Address
from Models.Product import ProductVariant
from Services.CartService import CartService

cartService = CartService()


class EmptyCartError(Exception):
    pass


class NoAddressError(Exception):
    pass


class InsufficientStockError(Exception):
    def __init__(self, productName: str, requested: int, available: int):
        self.productName = productName
        self.requested = requested
        self.available = available
        super().__init__(
            f"Stock insuficiente para '{productName}': "
            f"se pidieron {requested}, disponibles {available}"
        )


class OrderService:

    def getById(self, db: Session, orderId: int) -> Optional[Order]:
        return db.get(Order, orderId)

    def getByUser(self, db: Session, userId: int) -> List[Order]:
        stmt = select(Order).where(Order.userId == userId)
        return list(db.scalars(stmt).all())

    def _getInitialStatus(self, db: Session) -> OrderStatus:
        stmt = select(OrderStatus).where(OrderStatus.name == "Pending")
        status = db.scalars(stmt).first()
        if status is None:
            raise RuntimeError(
                "The 'Pending' OrderStatus doesn't exist in the database. "
                "Create it first (e.g. INSERT INTO order_status (name) VALUES ('Pending'))."
            )
        return status

    def createFromCart(self, db: Session, userId: int) -> Order:
        cart = cartService.getOrCreate(db, userId)
        if not cart.details:
            raise EmptyCartError("The cart is empty, can't generate the order")

        stmt = select(Address).where(Address.userId == userId)
        address = db.scalars(stmt).first()
        if address is None:
            raise NoAddressError("The user has no registered address")

        initialStatus = self._getInitialStatus(db)

        order = Order(
            userId=userId,
            addressId=address.addressId,
            orderStatusId=initialStatus.orderStatusId,
        )
        db.add(order)
        db.flush()

        for item in cart.details:
            variant = db.execute(
                select(ProductVariant)
                .where(ProductVariant.productVariantId == item.productVariantId)
                .with_for_update()
            ).scalar_one()

            if variant.stock < item.quantity:
                db.rollback()
                raise InsufficientStockError(
                    productName=variant.product.name,
                    requested=item.quantity,
                    available=variant.stock,
                )

            variant.stock -= item.quantity

            db.add(OrderDetail(
                orderId=order.orderId,
                productVariantId=item.productVariantId,
                quantity=item.quantity,
                price=item.unitPrice,
            ))

        cartService.empty(db, cart)

        db.commit()
        db.refresh(order)
        return order
