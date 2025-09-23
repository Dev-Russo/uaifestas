from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from database import Base

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
    event_date = Column(DateTime, nullable=False)
    image_url = Column(String, nullable=True)
    status = Column(String, default="active", nullable=False) # activate, cancelled, completed
    
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"))
    user = relationship("User", back_populates="events")
    
    products = relationship("Product", back_populates="event", cascade="all, delete-orphan")