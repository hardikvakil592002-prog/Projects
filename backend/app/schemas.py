from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator


class RegistrationBase(BaseModel):
    attendee_name: str = Field(..., min_length=1, max_length=255)
    attendee_email: EmailStr


class RegistrationCreate(RegistrationBase):
    pass


class Registration(RegistrationBase):
    id: int
    registered_at: datetime

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1024)
    location: str = Field(..., min_length=1, max_length=255)
    starts_at: datetime
    ends_at: datetime
    capacity: int = Field(..., gt=0)

    @validator("ends_at")
    def validate_ends_after_start(cls, value: datetime, values):
        starts_at = values.get("starts_at")
        if starts_at and value <= starts_at:
            raise ValueError("Event end time must be after the start time")
        return value


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    created_at: datetime
    registrations: List[Registration] = Field(default_factory=list)

    class Config:
        orm_mode = True
