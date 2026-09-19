from app.database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship

class Landlord(Base):
    __tablename__="landlords"
    landlord_id= Column(Integer,primary_key=True,index=True)
    landlord_name= Column(String(50),nullable=False,index=True)
    email=Column(String(100),unique=True,nullable=False,index=True)
    phone=Column(String(10),nullable=True)
    address=Column(String(100),nullable=True)
    password=Column(String(255),nullable=False)

    flats=relationship("Flat",back_populates="landlord",cascade="all,delete-orphan")
