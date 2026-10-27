from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Events(BaseModel):
    id: int
    title: str
    description: Optional[str]
    starts_at: datetime
    ends_at: datetime
    organiser_id: int
    venue_id: int
    venue_name: str
    venue_address: Optional[str]
    venue_capacity: Optional[int]

class EventsResponse(BaseModel):
    events: list[Events]