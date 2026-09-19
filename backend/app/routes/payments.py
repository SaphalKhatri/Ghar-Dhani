from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.models.lease import Lease
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(prefix="/api/payments", tags=["Payments"])


# Helper function to compute payment status based on amounts and due date
def determine_payment_status(amount_due: float, amount_paid: float, due_date: date) -> str:
    if amount_paid >= amount_due:
        return "paid"
    elif date.today() > due_date:
        return "overdue"
    elif amount_paid > 0:
        return "partial"
    else:
        return "pending"


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # Verify lease exists
    lease = db.query(Lease).filter(Lease.lease_id == payment.lease_id).first()
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lease with ID {payment.lease_id} not found.",
        )

    # Check if a payment for this billing month already exists for this lease
    existing_payment = (
        db.query(Payment)
        .filter(Payment.lease_id == payment.lease_id, Payment.billing_month == payment.billing_month)
        .first()
    )
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment for {payment.billing_month} already exists for this lease.",
        )

    # Determine status automatically
    status_calculated = determine_payment_status(
        amount_due=payment.amount_due,
        amount_paid=payment.amount_paid or 0.0,
        due_date=payment.due_date,
    )

    new_payment = Payment(
        lease_id=payment.lease_id,
        billing_month=payment.billing_month,
        amount_due=payment.amount_due,
        amount_paid=payment.amount_paid or 0.0,
        due_date=payment.due_date,
        status=status_calculated,
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


@router.get("/", response_model=List[PaymentResponse])
def get_all_payments(lease_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Payment)
    if lease_id:
        query = query.filter(Payment.lease_id == lease_id)
    return query.all()


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID {payment_id} not found.",
        )
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
def record_payment_amount(payment_id: int, payment_update: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with ID {payment_id} not found.",
        )

    # If amount_paid is updated, recalculate status automatically
    if payment_update.amount_paid is not None:
        payment.amount_paid = payment_update.amount_paid
        payment.status = determine_payment_status(
            amount_due=payment.amount_due,
            amount_paid=payment.amount_paid,
            due_date=payment.due_date,
        )

    # Allow manual override of status if explicitly sent
    if payment_update.status is not None:
        payment.status = payment_update.status

    db.commit()
    db.refresh(payment)
    return payment