# Schemas/Brand.py
from pydantic import BaseModel, ConfigDict, Field


class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=45)


class BrandOut(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    brandId: int
    brandUuid: str
