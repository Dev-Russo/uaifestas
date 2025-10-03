import uuid
from sqlalchemy import Column, DateTime, String, Float, ForeignKey, Integer   
from sqlalchemy.orm import relationship, declarative_base
from database import Base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import Base
from enums import SaleStatus

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    status = Column(String, default=SaleStatus.PAID, nullable=False) # Por padrão, toda venda já nasce "PAGA" Por ser vendas em dinheiro no momento
    payment_method = Column(String, default="dinheiro", nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    unique_code = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False, index=True)
    checked_at = Column(DateTime, nullable=True, default=None)
    canceled_at = Column(DateTime, nullable=True, default=None)
    sale_price = Column(Float, nullable=False)
    
    product = relationship("Product", back_populates="sales")
    seller = relationship("User", back_populates="sales")