# Services/AddressService.py
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from Models.User import Address
from Schemas.Address import AddressCreate, AddressUpdate


class AddressService:

    def getById(self, db: Session, addressId: int) -> Optional[Address]:
        return db.get(Address, addressId)

    def getByUser(self, db: Session, userId: int) -> List[Address]:
        stmt = select(Address).where(Address.userId == userId)
        return list(db.scalars(stmt).all())

    def create(self, db: Session, userId: int, addressIn: AddressCreate) -> Address:
        newAddress = Address(**addressIn.model_dump(), userId=userId)
        db.add(newAddress)
        db.commit()
        db.refresh(newAddress)
        return newAddress

    def update(self, db: Session, address: Address, changes: AddressUpdate) -> Address:
        data = changes.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(address, field, value)
        db.commit()
        db.refresh(address)
        return address

    def delete(self, db: Session, address: Address) -> None:
        db.delete(address)
        db.commit()
