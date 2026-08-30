# Models/Base.py
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def generateUuid() -> str:
    return str(uuid.uuid4())


class TimestampMixin:
    createdAt: Mapped[datetime] = mapped_column("created_at", DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, server_default=func.now(), onupdate=func.now()
    )
