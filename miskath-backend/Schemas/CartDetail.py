# Schemas/CartDetail.py
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from Schemas.Variant import VariantOutSimple


class CartDetailCreate(BaseModel):
    productVariantId: int
    quantity: int = Field(..., gt=0, description="Cantidad, debe ser mayor a 0")


class CartDetailUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cartDetailId: int
    cartDetailUuid: str
    quantity: int
    unitPrice: Decimal
    productVariant: VariantOutSimple
