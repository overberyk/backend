# Routes/UserRoutes.py
from typing import List

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from Config import getDb, limiter
from Controllers.UserController import UserController
from Controllers.AddressController import AddressController
from Schemas.User import UserCreate, UserOut, UserUpdate, UserChangeRole
from Schemas.Address import AddressCreate, AddressOut, AddressUpdate
from Security import requireRoles, verifyOwnerOrAdmin
from Models.User import User

UserRoutes = APIRouter(prefix="/users", tags=["Users"])
userController = UserController()
addressController = AddressController()


# ---------------------- Usuario ----------------------

@UserRoutes.get("/", response_model=List[UserOut])
def list(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin")),
):
    return userController.list(db, skip=skip, limit=limit)


@UserRoutes.get("/{userId}", response_model=UserOut)
def get(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return userController.get(db, userId)


@UserRoutes.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def create(request: Request, userIn: UserCreate, db: Session = Depends(getDb)):
    return userController.create(db, userIn)


@UserRoutes.patch("/{userId}", response_model=UserOut)
def update(
    userId: int,
    changes: UserUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return userController.update(db, userId, changes)


@UserRoutes.delete("/{userId}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.delete(db, userId)


@UserRoutes.patch("/{userId}/role", response_model=UserOut)
def changeRole(
    userId: int,
    change: UserChangeRole,
    db: Session = Depends(getDb),
    currentUser: User = Depends(requireRoles("admin")),
):
    return userController.changeRole(db, userId, change)


# ---------------------- Direcciones del usuario ----------------------

@UserRoutes.get("/{userId}/addresses", response_model=List[AddressOut])
def listAddresses(
    userId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return addressController.list(db, userId)


@UserRoutes.post(
    "/{userId}/addresses",
    response_model=AddressOut,
    status_code=status.HTTP_201_CREATED,
)
def createAddress(
    userId: int,
    addressIn: AddressCreate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    userController.getOrFail(db, userId)
    return addressController.create(db, userId, addressIn)


@UserRoutes.patch("/{userId}/addresses/{addressId}", response_model=AddressOut)
def updateAddress(
    userId: int,
    addressId: int,
    changes: AddressUpdate,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    return addressController.update(db, userId, addressId, changes)


@UserRoutes.delete("/{userId}/addresses/{addressId}", status_code=status.HTTP_204_NO_CONTENT)
def deleteAddress(
    userId: int,
    addressId: int,
    db: Session = Depends(getDb),
    currentUser: User = Depends(verifyOwnerOrAdmin),
):
    addressController.delete(db, userId, addressId)
