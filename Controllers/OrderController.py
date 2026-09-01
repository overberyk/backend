# Controllers/OrderController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.Order import Order
from Services.OrderService import (
    OrderService, EmptyCartError, NoAddressError, InsufficientStockError,
)

orderService = OrderService()


class OrderController:

    def getOrFail(self, db: Session, userId: int, orderId: int) -> Order:
        order = orderService.getById(db, orderId)
        if order is None or order.userId != userId:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pedido con id {orderId} no encontrado para este usuario",
            )
        return order

    def list(self, db: Session, userId: int):
        return orderService.getByUser(db, userId)

    def get(self, db: Session, userId: int, orderId: int) -> Order:
        return self.getOrFail(db, userId, orderId)

    def create(self, db: Session, userId: int) -> Order:
        try:
            return orderService.createFromCart(db, userId)
        except EmptyCartError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except NoAddressError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except InsufficientStockError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
