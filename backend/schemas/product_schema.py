from pydantic import BaseModel

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

    class Config:
        from_attributes = True