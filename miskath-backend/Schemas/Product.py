# Schemas/Product.py
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    categoryId: int
    name: str
    description: Optional[str] = None


class BrandOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    brandId: int
    name: str


class TypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    typeId: int
    name: str


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)
    description: Optional[str] = Field(default=None, max_length=500)
    unitPrice: Decimal = Field(..., gt=0, description="Precio unitario, debe ser mayor a 0")
    categoryId: int
    brandId: Optional[int] = None
    typeId: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=45)
    description: Optional[str] = Field(default=None, max_length=500)
    unitPrice: Optional[Decimal] = Field(default=None, gt=0)
    categoryId: Optional[int] = None
    brandId: Optional[int] = None
    typeId: Optional[int] = None


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    productId: int
    productUuid: str
    category: CategoryOut
    brand: Optional[BrandOut] = None
    type: Optional[TypeOut] = None


class ProductOutSimple(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    productId: int
    productUuid: str
    name: str
    unitPrice: Decimal
