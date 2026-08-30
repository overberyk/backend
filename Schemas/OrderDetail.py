# Schemas/OrderDetail.py
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from Schemas.Variant import VariantOutSimple


class OrderDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    orderDetailId: int
    orderDetailUuid: str
    quantity: int
    price: Decimal
    productVariant: VariantOutSimple
