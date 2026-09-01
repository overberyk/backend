# Schemas/Address.py
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AddressBase(BaseModel):
    city: str = Field(..., min_length=1, max_length=45)
    department: str = Field(..., min_length=1, max_length=45)
    neighborhood: Optional[str] = Field(default=None, max_length=45)
    streetAddress: str = Field(..., min_length=1, max_length=45)


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    city: Optional[str] = Field(default=None, min_length=1, max_length=45)
    department: Optional[str] = Field(default=None, min_length=1, max_length=45)
    neighborhood: Optional[str] = Field(default=None, max_length=45)
    streetAddress: Optional[str] = Field(default=None, min_length=1, max_length=45)


class AddressOut(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    addressId: int
    addressUuid: str
    userId: int
