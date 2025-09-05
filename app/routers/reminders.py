from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.reminder import ReminderCreate, ReminderResponse
from twilio.rest import Client
import os

router = APIRouter(prefix="/reminders", tags=["Reminders"])

# Twilio credentials from environment
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@router.post("/", response_model=ReminderResponse)
def create_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == reminder.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Make the call via Twilio
    call = twilio_client.calls.create(
        to=customer.phone,
        from_=TWILIO_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # replace with your own TwiML if needed
    )

    # Save reminder in DB
    db_reminder = models.Reminder(**reminder.dict(), call_sid=call.sid)
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return db_reminder
