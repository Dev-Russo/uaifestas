from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    name: str
    description: str | None = None
    street: str
    cep : str
    neighborhood: str
    number: str
    city: str
    created: datetime
    event_date: datetime
    image_url: str | None = None
    status: str = "active"
    
class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    
    class Config:
        from_attributes =  True