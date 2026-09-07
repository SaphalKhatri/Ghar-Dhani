from app.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Flat(Base):
    __tablename__ = "flats"

    flat_id = Column(Integer, primary_key=True, index=True)
    landlord_id = Column(Integer, ForeignKey("landlords.landlord_id"), nullable=False )
    flat_name = Column(String(100), nullable=False)
    rent_amount = Column(Float, nullable=False)
    status = Column(String(20), default="available", nullable=False )

    # Relationships
    landlord = relationship("Landlord", back_populates="flats")
    leases = relationship(
        "Lease", back_populates="flat", cascade="all, delete-orphan"
    )