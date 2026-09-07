from app.database import Base
from sqlalchemy import Columnm,Integer,String
from sqlalchemy.orm import relationship

class Landlord(Base):
    __tablename__="landlords"
    landlord_id= Columnm(Integer,primary_key=True,index=True)
    landlord_name= Columnm(String(50),nullable=False,index=True)
    email=Columnm(String(100),unique=True,nullable=False,index=True)
    phone=Columnm(String(10),nullable=True)
    address=Columnm(string(100),nullable=True)
    password=Columnm(string(255),nullable=False)

    flats=relationship("Flat",back_populates="landlord",cascade="all,delete-orphan")
