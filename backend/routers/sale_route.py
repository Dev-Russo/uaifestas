from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.utils.qrcode_utils import generate_qrcode_image_in_memory
from dependencies import get_db
from models import user_model, sale_model
from schemas import sale_schema
from utils.auth_utils import get_current_user
from utils.sale_utils import create_sale
from utils.email_utils import send_confirmation_email_sync
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

@router.post("/{id_sale}", response_model=sale_schema.Sale)
def resend_qrcode_mail(id: int, db: Session = Depends(get_db)):
    db_sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id).first()
    
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    try:
        qrcode_filepath = generate_qrcode_image_in_memory(str(db_sale.unique_code))
            
        formatted_date = db_sale.product.event.date.strftime("%d de %B de %Y às %H:%M")
            
        formatted_price = f"R$ {db_sale.product.price:.2f}".replace('.', ',')
            
        email_data = {
            "buyer_name": db_sale.buyer_name,
            "event_name": db_sale.product.event.name,
            "product_name": db_sale.product.name_product,
            "event_date": formatted_date,
            "event_location": db_sale.product.event.location,
            "product_price": formatted_price
        }
        
        send_confirmation_email_sync(
            recipient_email= db_sale.buyer_email,
            email_data=email_data,
            qrcode_buffer= qrcode_filepath
        )
    except Exception as e:
        print(f"ERRO AO ENVIAR EMAIL: {e}")
    finally:
        if qrcode_filepath and os.path.exists(qrcode_filepath):
            os.remove(qrcode_filepath)
            print(f"Arquivo temporário {qrcode_filepath} apagado.")

    return db_sale    
    