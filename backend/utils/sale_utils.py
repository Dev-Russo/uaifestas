from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import sale_models, product_model, user_model
from schemas import sale_schema

def create_sale(db: Session, sale: sale_schema.SaleCreate, seller_id: int | None = None) -> sale_models.Sale:
    product = db.query(product_model.Product).filter(product_model.Product.id_product == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    
    if seller_id:
        seller = db.get(user_model.User, seller_id)
        if not seller:
            raise HTTPException(status_code=404, detail="Seller Not Found")
    else:
        seller = None
    
    new_sale = sale_models.Sale(
        product_id = sale.product_id,
        seller_id = seller_id,
        buyer_name = sale.buyer_name,
        buyer_email = sale.buyer_email
    )
    
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    
    return new_sale