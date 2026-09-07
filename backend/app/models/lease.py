from app.database import Base 
from sqlalchemy import Column,String,Integer,Date
from sqlalchemy.orm import relationship

class Lease(Base):
    __tablename__="leases"
    lease_id=Column(Integer,primary_key=True,index=True)
    tenant_id=Column(Integer,ForeignKey(tenants.tenant_id),nullable=False)
    flat_id=Column(Integer,ForeignKey(flats.flat_id),nullable=False)
    start_date=Column(Date,nullable=False)
    end_date=Column(Date,nullable=True)
    status=Column(String,default="active")#active ot ended

    #relationships
    tenant=relationship("Tenant",back_populates="leases")
    flat=relationship("Flat",back_populates="leases")
    payments=relationship("Payment",back_populates="lease")