from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
import re

# Strict validation patterns
NAME_REGEX = re.compile(r"^[a-zA-Z\s]{1,100}$")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message content")
    session_id: str = Field(..., description="Unique session identifier (UUID)")

class ChatResponse(BaseModel):
    reply: str

class PatientData(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    query: Optional[str] = None

    @validator("name")
    def validate_name(cls, v):
        if v is not None:
            if not NAME_REGEX.match(v):
                raise ValueError("Name must contain only letters and spaces, and be 1-100 characters long.")
        return v

    @validator("age")
    def validate_age(cls, v):
        if v is not None:
            if not (0 <= v <= 120):
                raise ValueError("Age must be between 0 and 120.")
        return v

    @validator("query")
    def validate_query(cls, v):
        if v is not None:
            v = v.strip()
            if not (1 <= len(v) <= 500):
                raise ValueError("Query must be between 1 and 500 characters.")
        return v

class WebhookPayload(BaseModel):
    patient_name: str
    patient_age: int
    patient_query: str
    ward: Literal["general", "emergency", "mental_health"]
