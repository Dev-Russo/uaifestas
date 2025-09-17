from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from database import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable = False, index = True)
    description = Column(Text, nullable=False, index=True)
    location = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    
    products = relationship("Product", back_populates="event", cascade="all, delete-orphan")