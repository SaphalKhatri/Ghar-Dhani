from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    lease_id = Column(Integer, ForeignKey("leases.lease_id"), nullable=False)
    billing_month = Column(String, nullable=False)  # e.g., "2026-09" or "January 2026"
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="pending")  # 'pending', 'partial', 'paid', 'overdue'

    # Relationship
    lease = relationship("Lease", back_populates="payments")