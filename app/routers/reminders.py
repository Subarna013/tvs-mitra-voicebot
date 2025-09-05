from fastapi import APIRouter, BackgroundTasks
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os

router = APIRouter()

# Load environment variables (set these in Render or .env)
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH)

scheduler = BackgroundScheduler()
scheduler.start()

# Example database of customers (replace with your DB queries)
customers = [
    {"name": "Ravi Kumar", "phone": "+91XXXXXXXXXX", "emi_due_date": "2025-09-07", "emi_amount": 5000},
    {"name": "Anita Sharma", "phone": "+91YYYYYYYYYY", "emi_due_date": "2025-09-08", "emi_amount": 7000},
]


def make_call(phone_number: str, customer_name: str, emi_amount: int, emi_date: str):
    """Trigger Twilio call with TVS Credit EMI message."""
    message = f"Hello {customer_name}, this is TVS Mitra. Your EMI of ₹{emi_amount} is due on {emi_date}. Please pay on time. Thank you."

    twiml = VoiceResponse()
    twiml.say(message, voice='alice', language='en-IN')
    twiml.pause(length=1)
    twiml.say("Press 1 to confirm payment or 2 to speak with a customer support agent.", voice='alice')

    call = client.calls.create(
        twiml=str(twiml),
        to=phone_number,
        from_=TWILIO_NUMBER
    )
    print(f"Call initiated to {phone_number}, SID: {call.sid}")


@router.post("/send_reminders")
def send_reminders(background_tasks: BackgroundTasks):
    """Schedule EMI reminder calls for all customers whose EMI is due today."""
    today = datetime.now().date()

    for customer in customers:
        emi_date = datetime.strptime(customer["emi_due_date"], "%Y-%m-%d").date()
        if emi_date == today:
            # Schedule in background
            background_tasks.add_task(make_call, customer["phone"], customer["name"], customer["emi_amount"],
                                      customer["emi_due_date"])

    return {"status": "Reminders scheduled for today's EMI due customers."}


@router.post("/schedule_automatic_reminders")
def schedule_automatic_reminders():
    """Schedule daily automatic reminders at 9 AM."""
    scheduler.add_job(send_reminders, 'cron', hour=9, minute=0)
    return {"status": "Automatic daily EMI reminders scheduled at 9 AM."}
