from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from .product_schema import Product

class SaleBase(BaseModel):
    buyer_name: str
    buyer_email: EmailStr
    
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