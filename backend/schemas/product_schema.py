from pydantic import BaseModel
<<<<<<< HEAD

##Schemas mostra como os dados devem estar em formato Json

##Base do product (cliente envia)
class ProductBase(BaseModel):
    name_product: str
    description_product: str
    price: float

#Criar um produto novo
class ProductCreate(ProductBase):
    pass

##Ler um produto o que a API retorna
class Product(ProductBase):
    id: int
=======
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
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1

    class Config:
        from_attributes = True