from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utils.qrcode_utils import generate_qrcode_image_in_memory
from dependencies import get_db
from models import user_model, sale_model
from schemas import sale_schema
from utils.auth_utils import get_current_user
from utils.sale_utils import create_sale
from utils.email_utils import formated_email_to_send
import os

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
    return create_sale(db=db, sale=sale_data)

@router.post("/{id_sale}/resend", response_model=sale_schema.Sale)
def resend_qrcode_mail(id: int, db: Session = Depends(get_db)):
    db_sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id).first()
    
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    formated_email_to_send(db_sale)

    return db_sale    

@router.put("/{id_sale}/altermail", response_model=sale_schema.Sale)
def alter_mail_name(id: int, sale: sale_schema.SaleBase, db: Session = Depends(get_db)):
    db_sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id).first()
    
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    if sale.buyer_email is not None:
        db_sale.buyer_email = sale.buyer_email
    if sale.buyer_name is not None:
        db_sale.buyer_name = sale.buyer_name
    
    formated_email_to_send(db_sale)
    
    db.commit()
    db.refresh(db_sale)
    
    return db_sale

@router.get("/", response_model=list[sale_schema.Sale])
def get_all_sales(db: Session = Depends(get_db)):
    sales = db.query(sale_model.Sale).all()
    return sales

@router.get("/{id_sale}", response_model=sale_schema.Sale)
def get_sale_by_id(id_sale: int, db: Session = Depends(get_db)):    
    sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id_sale).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    return sale