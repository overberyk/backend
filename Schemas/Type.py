# Schemas/Type.py
from pydantic import BaseModel, ConfigDict, Field


class TypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)


class TypeCreate(TypeBase):
    pass


class TypeUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)


class TypeOut(TypeBase):
    model_config = ConfigDict(from_attributes=True)

    typeId: int
    typeUuid: str
