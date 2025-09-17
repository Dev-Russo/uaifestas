from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id_product = Column(Integer, primary_key = True)
    name_product = Column(String(100), nullable=False, index=True)
    description_product = Column(String, nullable=False)
    price = Column(Float, nullable=False)