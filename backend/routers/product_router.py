from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from models import product_model
from schemas import product_schema

router = APIRouter()

@router.post("/", response_model=product_schema.Product)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    db_product = product_model.Product(
        name_product = product.name_product,
        description_product = product.description_product,
        price = product.price
    )
    #Adiciona o objeto criado no banco de dados
    db.add(db_product)
    #Confirma e salva as mudanças
    db.commit()
    #Atualiza o objeto com os dados que o banco acabou de gerar (ID)
    db.refresh(db_product)

    return db_product
