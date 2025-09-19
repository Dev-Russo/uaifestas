from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import product_model, sale_model, user_model
from schemas import sale_schema
from .qrcode_utils import generate_qrcode_image_in_memory
from .email_utils import send_confirmation_email_sync

def create_sale(db: Session, sale: sale_schema.SaleCreate, seller_id: int | None = None) -> sale_model.Sale:
    product = db.query(product_model.Product).filter(product_model.Product.id_product == sale.product_id).first()
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
    
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    
    print(f"Venda {new_sale.id} criada. Gerando QR Code e enviando e-mail...")
    try:
        qrcode_filepath = generate_qrcode_image_in_memory(str(new_sale.unique_code))
        email_data = {"buyer_name": new_sale.buyer_name}
        send_confirmation_email_sync(
            recipient_email=new_sale.buyer_email,
            email_data=email_data,
            qrcode_buffer=qrcode_filepath
        )
        print(f"E-mail enviado com sucesso para {new_sale.buyer_email}.")
    except Exception as e:
        print(f"ERRO AO ENVIAR E-MAIL: {e}")

    
    return new_sale