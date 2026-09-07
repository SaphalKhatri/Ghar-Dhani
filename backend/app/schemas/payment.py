from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, computed_field


class PaymentBase(BaseModel):
    lease_id: int
    billing_month: str  # e.g. "2026-09" or "January 2026"
    amount_due: float
    amount_paid: Optional[float] = 0.0
    due_date: date
    status: Optional[str] = "pending"


# Used when creating a payment record
class PaymentCreate(PaymentBase):
    pass


# Used when recording a payment or updating payment details
class PaymentUpdate(BaseModel):
    amount_paid: Optional[float] = None
    status: Optional[str] = None


# Used when returning payment info in API responses
class PaymentResponse(BaseModel):
    payment_id: int
    lease_id: int
    billing_month: str
    amount_due: float
    amount_paid: float
    due_date: date
    status: str

    # Dynamically compute remaining amount so we don't need a column in the database
    @computed_field
    @property
    def remaining_amount(self) -> float:
        return max(0.0, self.amount_due - self.amount_paid)

    model_config = ConfigDict(from_attributes=True)