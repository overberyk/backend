# Schemas/Variant.py
from pydantic import BaseModel, ConfigDict

from Schemas.Product import ProductOutSimple


class VariantOutSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    productVariantId: int
    productVariantUuid: str
    stock: int
    product: ProductOutSimple
