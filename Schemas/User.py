# Schemas/User.py
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    roleId: int
    name: str


class UserBase(BaseModel):
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=45)
    birthDate: Optional[date] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72, description="Mínimo 8 caracteres")


class UserUpdate(BaseModel):
    firstName: Optional[str] = Field(default=None, min_length=1, max_length=50)
    lastName: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=45)
    birthDate: Optional[date] = None


class UserChangeRole(BaseModel):
    roleId: int


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    userId: int
    userUuid: str
    role: RoleOut
