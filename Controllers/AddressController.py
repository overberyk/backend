# Controllers/AddressController.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from Models.User import Address
from Schemas.Address import AddressCreate, AddressUpdate
from Services.AddressService import AddressService

addressService = AddressService()


class AddressController:

    def getOrFail(self, db: Session, userId: int, addressId: int) -> Address:
        address = addressService.getById(db, addressId)
        if address is None or address.userId != userId:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dirección con id {addressId} no encontrada para este usuario",
            )
        return address

    def list(self, db: Session, userId: int):
        return addressService.getByUser(db, userId)

    def create(self, db: Session, userId: int, addressIn: AddressCreate) -> Address:
        return addressService.create(db, userId, addressIn)

    def update(self, db: Session, userId: int, addressId: int, changes: AddressUpdate) -> Address:
        address = self.getOrFail(db, userId, addressId)
        return addressService.update(db, address, changes)

    def delete(self, db: Session, userId: int, addressId: int) -> None:
        address = self.getOrFail(db, userId, addressId)
        addressService.delete(db, address)
