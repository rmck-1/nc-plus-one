from pydantic import BaseModel
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

class ReturnCreatedEvent(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id: int
    organiser_id: int
    created_at: datetime

class NewEventResponse(BaseModel):
    event: ReturnCreatedEvent
