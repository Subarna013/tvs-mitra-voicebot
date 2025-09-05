# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True)
    loan_id = Column(String, unique=True, index=True)
    amount_due = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="DUE")
    ptp_date = Column(Date, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    loan_type = Column(String, nullable=True)
    region = Column(String, nullable=True)
    contact_attempts = Column(Integer, default=0)
    preferred_language = Column(String, default="en-IN")
    last_contacted = Column(Date, nullable=True)
    priority_score = Column(Integer, default=0)
    escalation_level = Column(Integer, default=0)

    payments = relationship("Payment", back_populates="customer")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    mode = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="payments")
