from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.enums import EventStatus
from models import product_model, sale_model, user_model, event_model
from schemas import sale_schema
from .qrcode_utils import generate_qrcode_image_in_memory
from .email_utils import  formated_email_to_send
import os

import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

def create_sale(db: Session, sale: sale_schema.SaleCreate, seller_id: int | None = None) -> sale_model.Sale:
    product = db.query(product_model.Product).filter(product_model.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")

    if product.event.status != EventStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Event is not active")

    if product.stock is not None:
        if product.stock <= 0:
            raise HTTPException(status_code=400, detail="Product Out of Stock")
        product.stock -= 1
    

    if seller_id:
        # Verificar se o vendedor é commissioner ou admin do evento
        seller = db.query(user_model.User).filter(user_model.User.id == seller_id).first()
        if not seller:
            raise HTTPException(status_code=404, detail="Seller Not Found")
        
        # Permitir que tanto commissioners quanto admins façam vendas comissionadas
        is_commissioner = seller in product.event.commissioners
        is_admin = seller in product.event.administrators
        
        if not (is_commissioner or is_admin):
            raise HTTPException(status_code=403, detail="User is not authorized to sell for this event")
    else:
        seller = None
    
    new_sale = sale_model.Sale(
        product_id = sale.product_id,
        seller_id = seller_id,
        buyer_name = sale.buyer_name,
        buyer_email = sale.buyer_email,
        sale_price = product.price
    )

    
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    
    print(f"Venda {new_sale.id} criada. Gerando QR Code e enviando e-mail...")
    
    formated_email_to_send(new_sale)

    
    return new_sale

def validate_event_admin_access(db: Session, current_user: user_model.User, id_event: int):
    event = db.query(event_model.Event).filter(event_model.Event.id == id_event).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    if current_user in event.administrators:
        return "admin"

    if current_user in event.commissioners:
        return "commissioner"
    
    raise HTTPException(status_code=403, detail="Operation not permitted: user is not an administrator or commissioner of this event")