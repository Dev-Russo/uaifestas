<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, Float
=======
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1
from database import Base

class Product(Base):
    __tablename__ = "products"
<<<<<<< HEAD

    id_product = Column(Integer, primary_key= True)
    name_product = Column(String(100), nullable=False, index=True)
    description_product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
=======
    
    id_product = Column(Integer, primary_key = True)
    name_product = Column(String(100), nullable=False, index=True)
    description_product = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    
    event_id = Column(Integer, ForeignKey('events.id', ondelete="CASCADE"), nullable=False)
    
    event = relationship("Event", back_populates="products")
    sales = relationship("Sale", back_populates="product") 
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1
