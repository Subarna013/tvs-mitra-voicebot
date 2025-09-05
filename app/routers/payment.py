from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.db import models

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == payment.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Prevent overpayment
    if customer.amount_due < payment.amount_paid:
        raise HTTPException(status_code=400, detail="Payment exceeds due amount")

    # Create payment record
    db_payment = models.Payment(**payment.dict())
    db.add(db_payment)

    # Update customer's amount_due
    customer.amount_due -= payment.amount_paid
    if customer.amount_due == 0:
        customer.status = "CLEARED"

    db.commit()
    db.refresh(db_payment)
    db.refresh(customer)

    return db_payment
