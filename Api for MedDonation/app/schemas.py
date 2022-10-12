from ast import Pass
import email
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from app.database import Base

class MedBase(BaseModel):
    med_name: str
    quantity: int
    expiry: str
    status: str
    description: str
    saltname: str
    donationtime: str

class MedCreate(MedBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    dob: str
    phone: str
    created_at: datetime
    class Config:
        orm_mode = True
        
class Med(MedBase):
    med_id: int
    owner_id: int
    owner: UserOut
    class Config:
        orm_mode = True


class DonationBase(BaseModel):
    donationtype: str
    ngoname: str
    dateselected: str

class DonationCreate(DonationBase):
    pass

class Donation(DonationBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
        
# class Reque(BaseModel):
#     toy_id: int
#     exchange_toy_id: int
#     class Config:
#         orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    dob: str

class UserUpdate(BaseModel):
    email: EmailStr
    #password: str
    name: str
    dob: str
    phone: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token = str
    token_type = str

class TokenData(BaseModel):
    id: Optional[str] = None

class Request(BaseModel):
    med_id: int
    # owner_id: int
    ownerof_med: int
    approval: Optional[str] = "Empty"
class RequestWithQuant(BaseModel):
    med_id: int
    ownerof_med: int
    approval: Optional[str] = "Empty"
    reqquantity: int








