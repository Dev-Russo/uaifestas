from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    date: datetime
    location: str
    description: str | None = None
    
class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    
    class Config:
        from_attributes =  True