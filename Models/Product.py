# Models/Product.py
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models.Base import Base, generateUuid


class Category(Base):
    __tablename__ = "category"

    categoryId: Mapped[int] = mapped_column("category_id", primary_key=True, autoincrement=True)
    categoryUuid: Mapped[str] = mapped_column("category_uuid", String(45), unique=True, default=generateUuid)
    name: Mapped[str] = mapped_column(String(45), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(100))

    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Brand(Base):
    __tablename__ = "brand"

    brandId: Mapped[int] = mapped_column("brand_id", primary_key=True, autoincrement=True)
    brandUuid: Mapped[str] = mapped_column("brand_uuid", String(45), unique=True, default=generateUuid)
    name: Mapped[str] = mapped_column(String(45), unique=True)

    products: Mapped[List["Product"]] = relationship(back_populates="brand")


class Size(Base):
    __tablename__ = "size"

    sizeId: Mapped[int] = mapped_column("size_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(3))

    variants: Mapped[List["ProductVariant"]] = relationship(back_populates="size")


class Type(Base):
    __tablename__ = "type"

    typeId: Mapped[int] = mapped_column("type_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(45))

    products: Mapped[List["Product"]] = relationship(back_populates="type")


class Color(Base):
    __tablename__ = "color"

    colorId: Mapped[int] = mapped_column("color_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15))

    variants: Mapped[List["ProductVariant"]] = relationship(back_populates="color")


class Product(Base):
    __tablename__ = "product"

    productId: Mapped[int] = mapped_column("product_id", primary_key=True, autoincrement=True)
    productUuid: Mapped[str] = mapped_column("product_uuid", String(45), unique=True, default=generateUuid)
    name: Mapped[str] = mapped_column(String(45))
    description: Mapped[Optional[str]] = mapped_column(Text)
    unitPrice: Mapped[Decimal] = mapped_column("unit_price", Numeric(10, 2))

    categoryId: Mapped[int] = mapped_column("category_id", ForeignKey("category.category_id"))
    brandId: Mapped[Optional[int]] = mapped_column("brand_id", ForeignKey("brand.brand_id"))
    typeId: Mapped[Optional[int]] = mapped_column("type_id", ForeignKey("type.type_id"))

    category: Mapped["Category"] = relationship(back_populates="products")
    brand: Mapped[Optional["Brand"]] = relationship(back_populates="products")
    type: Mapped[Optional["Type"]] = relationship(back_populates="products")
    variants: Mapped[List["ProductVariant"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(back_populates="product")


class ProductVariant(Base):
    __tablename__ = "product_variant"

    productVariantId: Mapped[int] = mapped_column("product_variant_id", primary_key=True, autoincrement=True)
    productVariantUuid: Mapped[str] = mapped_column(
        "product_variant_uuid", String(45), unique=True, default=generateUuid
    )

    productId: Mapped[int] = mapped_column("product_id", ForeignKey("product.product_id"))
    sizeId: Mapped[int] = mapped_column("size_id", ForeignKey("size.size_id"))
    colorId: Mapped[int] = mapped_column("color_id", ForeignKey("color.color_id"))
    stock: Mapped[int] = mapped_column(default=0)

    product: Mapped["Product"] = relationship(back_populates="variants")
    size: Mapped["Size"] = relationship(back_populates="variants")
    color: Mapped["Color"] = relationship(back_populates="variants")
    cartDetails: Mapped[List["CartDetail"]] = relationship(back_populates="productVariant")
    orderDetails: Mapped[List["OrderDetail"]] = relationship(back_populates="productVariant")
