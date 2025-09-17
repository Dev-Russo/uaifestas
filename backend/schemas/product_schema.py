from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name_product: str
    description_product: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    event_id: int

class Product(ProductBase):
    id_product: int
    event_id: int

    class Config:
        from_attributes = True