from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .association_tables import event_administrators_table
from database import Base
from enums import EventStatus

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable = False, index = True)
    description = Column(Text, nullable=False, index=True)
    street = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    number = Column(String, nullable=False)
    city = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)
    event_date = Column(DateTime, nullable=True)
    image_url = Column(String, nullable=True)
    status = Column(String, default=EventStatus.ACTIVE, nullable=False) # activate, cancelled, completed
    
    administrators = relationship(
        "User",
        secondary=event_administrators_table,
        back_populates="events"
    )
    
    comissioner = relationship(
        "User",
        secondary="comissioner_events",
        back_populates="comissioned_events"
    )

    products = relationship("Product", back_populates="event", cascade="all, delete-orphan")