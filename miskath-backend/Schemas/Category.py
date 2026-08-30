# Schemas/Category.py
from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)
    description: str = Field(..., min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)
    description: str = Field(..., min_length=1, max_length=100)


class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    categoryId: int
    categoryUuid: str
