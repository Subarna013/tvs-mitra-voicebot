# app/schemas/payment.py
from pydantic import BaseModel, Field
from datetime import date

class PaymentBase(BaseModel):
    customer_id: int
    amount_paid: float = Field(..., ge=0)
    payment_date: date
    mode: str  # e.g., "UPI", "Bank Transfer"

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    class Config:
        orm_mode = True
