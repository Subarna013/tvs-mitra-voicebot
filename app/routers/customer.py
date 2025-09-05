# app/routers/customer.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.crud import customer as crud
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/customers", tags=["Customers"])

# -------------------------------
# Endpoints
# -------------------------------

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        existing = crud.get_customer_by_phone_or_loan(db, customer.phone, customer.loan_id)
        if existing:
            raise HTTPException(status_code=409, detail="Customer already exists")
        return crud.create_customer(db, customer)
    except HTTPException:   # Let real HTTP errors pass through
        raise
    except Exception as e:  # Only catch unexpected ones
        logger.error(f"Error creating customer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    status: Optional[str] = None,
    region: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.list_customers(db, skip=skip, limit=limit, status=status, region=region)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud.update_customer(db, db_customer, customer_update.dict(exclude_unset=True))


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    crud.delete_customer(db, db_customer)
    return {"detail": "Deleted successfully"}


@router.get("/priority-queue/", response_model=List[CustomerResponse])
def priority_queue(limit: int = 50, db: Session = Depends(get_db)):
    return crud.get_priority_queue(db, limit)
