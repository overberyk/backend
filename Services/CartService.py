# Services/CartService.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.Cart import Cart, CartDetail
from Models.Product import ProductVariant
from Schemas.CartDetail import CartDetailCreate, CartDetailUpdate


class VariantNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    def __init__(self, requested: int, available: int):
        self.requested = requested
        self.available = available
        super().__init__(
            f"Stock insuficiente: se pidieron {requested}, disponibles {available}"
        )


class CartService:

    def getOrCreate(self, db: Session, userId: int) -> Cart:
        stmt = select(Cart).where(Cart.userId == userId)
        cart = db.scalars(stmt).first()
        if cart is not None:
            return cart

        cart = Cart(userId=userId)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    def getDetailById(self, db: Session, detailId: int) -> Optional[CartDetail]:
        return db.get(CartDetail, detailId)

    def addItem(self, db: Session, cart: Cart, itemIn: CartDetailCreate) -> CartDetail:
        variant = db.get(ProductVariant, itemIn.productVariantId)
        if variant is None:
            raise VariantNotFoundError(
                f"No existe una variante con id {itemIn.productVariantId}"
            )

        stmt = select(CartDetail).where(
            CartDetail.cartId == cart.cartId,
            CartDetail.productVariantId == itemIn.productVariantId,
        )
        existing = db.scalars(stmt).first()

        alreadyInCart = existing.quantity if existing is not None else 0
        totalRequested = alreadyInCart + itemIn.quantity

        if variant.stock < totalRequested:
            raise InsufficientStockError(requested=totalRequested, available=variant.stock)

        if existing is not None:
            existing.quantity = totalRequested
            db.commit()
            db.refresh(existing)
            return existing

        newItem = CartDetail(
            cartId=cart.cartId,
            productVariantId=itemIn.productVariantId,
            quantity=itemIn.quantity,
            unitPrice=variant.product.unitPrice,
        )
        db.add(newItem)
        db.commit()
        db.refresh(newItem)
        return newItem

    def updateItem(self, db: Session, detail: CartDetail, changes: CartDetailUpdate) -> CartDetail:
        variant = detail.productVariant
        if variant.stock < changes.quantity:
            raise InsufficientStockError(requested=changes.quantity, available=variant.stock)

        detail.quantity = changes.quantity
        db.commit()
        db.refresh(detail)
        return detail

    def deleteItem(self, db: Session, detail: CartDetail) -> None:
        db.delete(detail)
        db.commit()

    def empty(self, db: Session, cart: Cart) -> None:
        for detail in list(cart.details):
            db.delete(detail)
        db.commit()
