# Controllers/CartController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Cart import Cart, CartDetail
from Schemas.CartDetail import CartDetailCreate, CartDetailUpdate
from Services.CartService import CartService, VariantNotFoundError, InsufficientStockError

cartService = CartService()


class CartController:

    def getItemOrFail(self, db: Session, cartId: int, detailId: int) -> CartDetail:
        detail = cartService.getDetailById(db, detailId)
        if detail is None or detail.cartId != cartId:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item con id {detailId} no encontrado en este carrito",
            )
        return detail

    def get(self, db: Session, userId: int) -> Cart:
        return cartService.getOrCreate(db, userId)

    def addItem(self, db: Session, userId: int, itemIn: CartDetailCreate) -> CartDetail:
        cart = cartService.getOrCreate(db, userId)
        try:
            return cartService.addItem(db, cart, itemIn)
        except VariantNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except InsufficientStockError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    def updateItem(self, db: Session, userId: int, detailId: int, changes: CartDetailUpdate) -> CartDetail:
        cart = cartService.getOrCreate(db, userId)
        detail = self.getItemOrFail(db, cart.cartId, detailId)
        try:
            return cartService.updateItem(db, detail, changes)
        except InsufficientStockError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    def deleteItem(self, db: Session, userId: int, detailId: int) -> None:
        cart = cartService.getOrCreate(db, userId)
        detail = self.getItemOrFail(db, cart.cartId, detailId)
        cartService.deleteItem(db, detail)

    def empty(self, db: Session, userId: int) -> None:
        cart = cartService.getOrCreate(db, userId)
        cartService.empty(db, cart)
