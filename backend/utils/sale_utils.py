from sqlalchemy.orm import Session
from fastapi import HTTPException
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
    
    if seller_id:
        seller = db.get(user_model.User, seller_id)
        if not seller:
            raise HTTPException(status_code=404, detail="Seller Not Found")
    else:
        seller = None
    
    new_sale = sale_model.Sale(
        product_id = sale.product_id,
        seller_id = seller_id,
        buyer_name = sale.buyer_name,
        buyer_email = sale.buyer_email
    )

    if product.stock is not None:
        if product.stock <= 0:
            raise HTTPException(status_code=400, detail="Product Out of Stock")
        product.stock -= 1
    
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

    if current_user in event.comissioner:
        return "commissioner"
    
    raise HTTPException(status_code=403, detail="Operation not permitted: user is not an administrator or commissioner of this event")