from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
import uuid
from .product_schema import Product

class SaleBase(BaseModel):
    buyer_name: str
    buyer_email: EmailStr
    
    @validator('buyer_name')
    def validate_buyer_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Nome do comprador é obrigatório')
        if len(v.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        return v.strip()
    
    @validator('buyer_email')
    def validate_buyer_email(cls, v):
        if not v or "@" not in v:
            raise ValueError('Email inválido')
        return v.lower()
    
class SaleCreate(SaleBase):
    product_id: int
    
class Sale(SaleBase):
    id: int
    seller_id: int | None = None
    sale_date: datetime
    unique_code: uuid.UUID
    checked_at: datetime | None = None
    product: Product

    class Config:
        from_attributes = True