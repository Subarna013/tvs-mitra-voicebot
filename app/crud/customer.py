from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.db import models

# -------------------------------
# Helper functions
# -------------------------------

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_phone_or_loan(db: Session, phone: str, loan_id: str):
    """Check if a customer exists by phone or loan_id."""
    return db.query(models.Customer).filter(
        or_(models.Customer.phone == phone, models.Customer.loan_id == loan_id)
    ).first()

# -------------------------------
# CRUD operations
# -------------------------------

def create_customer(db: Session, customer):
    if get_customer_by_phone_or_loan(db, customer.phone, customer.loan_id):
        return None
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, db_customer, update_data: dict):
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, db_customer):
    db.delete(db_customer)
    db.commit()

def list_customers(db: Session, skip: int = 0, limit: int = 100, status=None, region=None):
    query = db.query(models.Customer)
    if status:
        query = query.filter(models.Customer.status == status)
    if region:
        query = query.filter(models.Customer.region == region)
    return query.offset(skip).limit(limit).all()

def get_priority_queue(db: Session, limit: int = 50):
    return db.query(models.Customer)\
        .filter(models.Customer.status.in_(["DUE", "BROKEN_PROMISE"]))\
        .order_by(desc(models.Customer.priority_score))\
        .limit(limit)\
        .all()
