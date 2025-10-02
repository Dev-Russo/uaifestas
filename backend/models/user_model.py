from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from .association_tables import event_administrators_table
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    events = relationship(
        "Event",
        secondary=event_administrators_table,
        back_populates="administrators"
    )
    sales = relationship("Sale", back_populates="seller")

    comissioned_events = relationship("Event", secondary="comissioner_events", back_populates="comissioners")