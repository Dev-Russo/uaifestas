from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    stock: Optional[int] = None
    price: float
    image_url: Optional[str] = None
    status: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    event_id: int

    class Config:
        from_attributes = True