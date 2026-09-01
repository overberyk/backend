# Schemas/Variant.py
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from Schemas.Product import ProductOutSimple


class VariantOutSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    productVariantId: int
    productVariantUuid: str
    stock: int
    product: ProductOutSimple


# ---------------------- Size ----------------------

class SizeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=3)


class SizeCreate(SizeBase):
    pass


class SizeUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=3)


class SizeOut(SizeBase):
    model_config = ConfigDict(from_attributes=True)

    sizeId: int


# ---------------------- Color ----------------------

class ColorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=15)


class ColorCreate(ColorBase):
    pass


class ColorUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=15)


class ColorOut(ColorBase):
    model_config = ConfigDict(from_attributes=True)

    colorId: int


# ---------------------- ProductVariant ----------------------

class ProductVariantBase(BaseModel):
    productId: int
    sizeId: int
    colorId: int
    stock: int = Field(default=0, ge=0)


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantUpdate(BaseModel):
    sizeId: Optional[int] = None
    colorId: Optional[int] = None
    stock: Optional[int] = Field(default=None, ge=0)


class ProductVariantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    productVariantId: int
    productVariantUuid: str
    productId: int
    sizeId: int
    colorId: int
    stock: int
