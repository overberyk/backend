# Schemas/Order.py
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, computed_field

from Schemas.Address import AddressOut
from Schemas.OrderDetail import OrderDetailOut


class OrderStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderStatusId: int
    name: str


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderId: int
    orderUuid: str
    userId: int
    address: AddressOut
    orderStatus: OrderStatusOut
    orderDetail: List[OrderDetailOut] = []

    @computed_field
    @property
    def total(self) -> Decimal:
        return sum(
            (d.price * d.quantity for d in self.orderDetail),
            start=Decimal("0"),
        )
