from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

class Events(BaseModel):
    id: int
    title: str
    description: Optional[str]
    starts_at: datetime
    ends_at: datetime
    venue_name: str
    venue_address: Optional[str]
    venue_capacity: Optional[int]

class EventsResponse(BaseModel):
    events: list[Events]

class Event(BaseModel):
    id: int
    title: str
    description: Optional[str] 
    starts_at: datetime
    ends_at: datetime
    venue_name: str
    venue_address: Optional[str] 
    venue_capacity: Optional[int]
    created_at: datetime 

class EventResponse(BaseModel):
    event: Event

class CreateEvent(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int

class ReturnEvent(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int
    organiser_id: int
    created_at: datetime

class ReturnEventResponse(BaseModel):
    event: ReturnEvent

class PatchEvent(BaseModel):
    description: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

    @model_validator(mode='after')
    def check_dates_are_valid(self):
        if self.starts_at and self.ends_at:
            if self.starts_at >= self.ends_at:
                raise ValueError("starts_at must be before ends_at")
        return self
