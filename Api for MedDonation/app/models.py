from ast import Str
from datetime import datetime
from email.policy import default
import imp
from psycopg2 import Date
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Medicine(Base):
    __tablename__ = "medicine"
    med_id = Column(Integer, primary_key=True, nullable=False)
    med_name = Column(String, nullable=False)
    expiry = Column(String, nullable=False)
    status = Column(String,nullable=False)
    quantity = Column(Integer, nullable=False)
    saltname = Column(String,nullable=False)
    description = Column(String, nullable = False)
    donationtime = Column(String, nullable = False)
    owner_id =Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    phone = Column(String, default="Empty")
    

class Request(Base):
    __tablename__ = "requests"
    owner_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    med_id = Column(Integer, ForeignKey("medicine.med_id"), primary_key=True)
    approval = Column(String, default="Empty")
    ownerof_med = Column(Integer, nullable=False)
    requested_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    reqquantity = Column(Integer)


class BarcodeMed(Base):
    __tablename__ = "barcode"
    id = Column(Integer, primary_key=True, nullable=False)
    barcode = Column(String, nullable=False)
    med_name = Column(String, nullable=False)
    expiry = Column(String, nullable=False)

class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, nullable=False)
    donationtype = Column(String, nullable=False)
    ngoname = Column(String, nullable=False)
    dateselected = Column(String, nullable=False)
    owner_id =Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")
    
    
    
    

