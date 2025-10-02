from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ComissionerEvent(Base):
    __tablename__ = "comissioner_events"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    created_at = Column(Integer, default=lambda: int(datetime.utcnow().timestamp()))
    
    user = relationship("User")
    event = relationship("Event")