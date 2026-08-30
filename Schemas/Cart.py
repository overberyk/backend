# Schemas/Cart.py
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, computed_field

from Schemas.CartDetail import CartDetailOut


class CartOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cartId: int
    cartUuid: str
    userId: int
    details: List[CartDetailOut] = []

    @computed_field
    @property
    def total(self) -> Decimal:
        return sum(
            (d.unitPrice * d.quantity for d in self.details),
            start=Decimal("0"),
        )
