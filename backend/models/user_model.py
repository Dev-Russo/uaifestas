from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    sales = relationship("Sale", back_populates="seller")