# Models/User.py
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Models.Base import Base, generateUuid, TimestampMixin


class Role(Base):
    __tablename__ = "role"

    roleId: Mapped[int] = mapped_column("role_id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(10))

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"<Role_id={self.roleId} name={self.name!r}>"


class User(Base, TimestampMixin):
    __tablename__ = "user"

    userId: Mapped[int] = mapped_column("user_id", primary_key=True, autoincrement=True)
    userUuid: Mapped[str] = mapped_column("user_uuid", String(45), unique=True, default=generateUuid)
    firstName: Mapped[str] = mapped_column("first_name", String(50))
    lastName: Mapped[str] = mapped_column("last_name", String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(45))
    birthDate: Mapped[Optional[date]] = mapped_column("birth_date", Date)
    passwordHash: Mapped[str] = mapped_column("password_hash", String(255))

    roleId: Mapped[int] = mapped_column("role_id", ForeignKey("role.role_id"))

    role: Mapped["Role"] = relationship(back_populates="users")
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    carts: Mapped[List["Cart"]] = relationship(back_populates="user")
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    refreshTokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User_id={self.userId} email={self.email!r}>"


class Address(Base):
    __tablename__ = "address"

    addressId: Mapped[int] = mapped_column("address_id", primary_key=True, autoincrement=True)
    addressUuid: Mapped[str] = mapped_column("address_uuid", String(45), unique=True, default=generateUuid)
    city: Mapped[str] = mapped_column(String(45))
    department: Mapped[str] = mapped_column(String(45))
    neighborhood: Mapped[Optional[str]] = mapped_column(String(45))
    streetAddress: Mapped[str] = mapped_column("street_address", String(45))

    userId: Mapped[int] = mapped_column("user_id", ForeignKey("user.user_id"))

    user: Mapped["User"] = relationship(back_populates="addresses")
    orders: Mapped[List["Order"]] = relationship(back_populates="address")

    def __repr__(self) -> str:
        return f"<Address_id={self.addressId} city={self.city!r}>"


class Comment(Base, TimestampMixin):
    __tablename__ = "comment"

    commentId: Mapped[int] = mapped_column("comment_id", primary_key=True, autoincrement=True)
    commentUuid: Mapped[str] = mapped_column("comment_uuid", String(45), unique=True, default=generateUuid)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    rating: Mapped[Optional[int]] = mapped_column()

    userId: Mapped[int] = mapped_column("user_id", ForeignKey("user.user_id"))
    productId: Mapped[int] = mapped_column("product_id", ForeignKey("product.product_id"))

    user: Mapped["User"] = relationship(back_populates="comments")
    product: Mapped["Product"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<Coment_id={self.commentId} rating={self.rating}>"


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    refreshTokenId: Mapped[int] = mapped_column("refresh_token_id", primary_key=True, autoincrement=True)
    tokenHash: Mapped[str] = mapped_column("token_hash", String(64), unique=True, index=True)
    userId: Mapped[int] = mapped_column("user_id", ForeignKey("user.user_id"))
    expiresAt: Mapped[datetime] = mapped_column("expires_at", DateTime)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    createdAt: Mapped[datetime] = mapped_column("created_at", DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="refreshTokens")

    def __repr__(self) -> str:
        return f"<RefreshToken_id={self.refreshTokenId} user_id={self.userId} revoked={self.revoked}>"
