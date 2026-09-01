# Schemas/Payment.py
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentMethodOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    paymentMethodId: int
    name: str


class PaymentStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    paymentStatusId: int
    name: str


class PaymentCreate(BaseModel):
    paymentMethodId: int


class PaymentConfirm(BaseModel):
    paymentStatusId: int


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    paymentId: int
    paymentUuid: str
    total: Decimal
    orderId: Optional[int] = None
    paymentMethod: PaymentMethodOut
    paymentStatus: PaymentStatusOut
