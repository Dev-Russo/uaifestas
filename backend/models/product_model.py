from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id_product = Column(Integer, primary_key = True)
    name_product = Column(String(100), nullable=False, index=True)
    description_product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    stack = Column(Integer, nullable=False)
    
    event_id = Column(Integer, ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    
    event = relationship("Event", back_populates="products")
    sales = relationship("Sale", back_populates="product") 
