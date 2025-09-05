from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from pydantic import BaseModel
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    name: str
    phone: str
    loan_id: str
    amount_due: float = Field(..., ge=0)
    due_date: date
    # Add all optional fields here
    status: Optional[str] = "DUE"
    ptp_date: Optional[date] = None
    sentiment_score: Optional[float] = None
    notes: Optional[str] = None
    loan_type: Optional[str] = None
    region: Optional[str] = None
    contact_attempts: Optional[int] = 0
    preferred_language: Optional[str] = "en-IN"
    last_contacted: Optional[date] = None
    priority_score: Optional[int] = 0
    escalation_level: Optional[int] = 0

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    loan_id: Optional[str] = None
    amount_due: Optional[float] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    ptp_date: Optional[date] = None
    sentiment_score: Optional[float] = None
    notes: Optional[str] = None
    loan_type: Optional[str] = None
    region: Optional[str] = None
    contact_attempts: Optional[int] = None
    preferred_language: Optional[str] = None
    last_contacted: Optional[date] = None
    priority_score: Optional[int] = None
    escalation_level: Optional[int] = None


class CustomerResponse(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
