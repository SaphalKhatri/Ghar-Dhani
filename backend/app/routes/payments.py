from datetime import date
from typing import List,Optional
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.models.lease import Lease
from app.schemas.payment import PaymentResponse,PaymentResponse,PaymentResponse,PaymentCreate

router=APIRouter(prefix="/api/payments",tags=["payments"])

def determine_payment_status(amount_due:float,amount_paid:float,due_date:date)->str:
    if amount_paid>= amount_due:
        return "paid"
    elif date.today() > due_date:
        return "overdue"
    elif amount_paid >0:
        return "partial"
    else:
        return "pending"

@router.post("/",response_model=PaymentResponse,status_code=staus.HTTP_201_CREATED)
def create_payment(payment:PaymentCreate,db:Session=Depends(get_db)):

    lease=db.query(Lease).filter(Lease.lease_id==payment.lease_id).first()
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"user of id{lease_id} not found"
        )
    #for checking for ths billing month already exists for the lease
    existing_lease=(
        db.query(Payment).filter(Payment.lease_id==payment.lease_id,Payment.billing_month==payment.billing_month).first()
    )
    if existing_lease()
