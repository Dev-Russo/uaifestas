import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Integer   
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import Base

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    
    sale_date = Column(datetime, default=datetime.utcnow, nullable=False)
    
    unique_code = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    
    product = relationship("Product", back_populates="sales")
    user = relationship("User", back_populates="sales")