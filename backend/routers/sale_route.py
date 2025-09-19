from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models import user_model # Necessário para o Depends(get_current_user)
from schemas import sale_schema
from utils.auth_utils import get_current_user
from utils.sale_utils import create_sale

router = APIRouter()

@router.post("/commissioned", response_model=sale_schema.Sale)
def create_commissioned_sale(
    sale_data: sale_schema.SaleCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    
    return create_sale(db=db, sale=sale_data, seller_id=current_user.id)

@router.post("/", response_model=sale_schema.Sale)
def create_sale_site(
    sale_data: sale_schema.SaleCreate,
    db: Session = Depends(get_db),
):
    db
    
    return create_sale(db=db, sale=sale_data)