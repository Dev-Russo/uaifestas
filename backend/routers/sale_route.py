from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.qrcode_utils import generate_qrcode_image_in_memory
from dependencies import get_db
from models import user_model, sale_model, product_model, event_model
from schemas import sale_schema
from utils.auth_utils import get_current_user
from utils.sale_utils import create_sale, validate_event_admin_access
from utils.email_utils import formated_email_to_send
from typing import Optional, List
from enums import SaleStatus
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
    current_user: user_model.User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "commissioner", "client"]:
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins, commissioners and clients can create sales")

    return create_sale(db=db, sale=sale_data)

@router.post("/{id_sale}/resend", response_model=sale_schema.Sale)
def resend_qrcode_mail(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    if current_user.role not in ["admin", "commissioner"]:
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins and commissioners can resend sale emails")
    
    db_sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id).first()
    
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    formated_email_to_send(db_sale)

    return db_sale

@router.put("/{id_sale}/altermail", response_model=sale_schema.Sale)
def alter_mail_name(
    id: int,
    sale: sale_schema.SaleBase, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    if current_user.role not in ["admin", "commissioner"]:
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins and commissioners can alter sale email or name")
    
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

@router.get("/", response_model=List[sale_schema.Sale])
def get_all_sales_by_event(
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user),
        event_id: int | None = None,
        product_id: Optional[int] = None,
        seller_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ):
    query = db.query(sale_model.Sale)
    if current_user.role == "commissioner":
        query = db.query(sale_model.Sale)
        query = query.join(sale_model.Sale.product).join(product_model.Product.event)
        query = query.filter(
            event_model.Event.id == event_id,  
            event_model.Event.comissioner_id == current_user.id  
        )
        
    elif current_user.role == "admin":
        if event_id:
            query = query.join(sale_model.Sale.product).join(product_model.Product.event)
            
            query = query.filter(
                event_model.Event.id == event_id,
                event_model.Event.comissioner_id == current_user.id 
            )
        
    else:
        admin_events_subquery = db.query(event_model.Event.id)\
                                  .filter(event_model.Event.comissioner_id == current_user.id)\
                                  .subquery()
                                  
        query = query.join(sale_model.Sale.product)\
                     .filter(product_model.Product.event_id.in_(admin_events_subquery))
    if seller_id:
        query = query.filter(sale_model.Sale.seller_id == seller_id)
        
    if product_id:
        query = query.filter(sale_model.Sale.product_id == product_id)
    
    query = query.offset(skip).limit(limit)
    sales = query.all()
    
    return sales

@router.get("/{id_sale}", response_model=sale_schema.Sale)
def get_sale_by_id(id_sale: int, db: Session = Depends(get_db)):
    sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id_sale).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    return sale

@router.post("/check/{unique_code}", response_model=sale_schema.Sale)
def check_in_sale(
    unique_code: str, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    db_event = db.query(event_model.Event).join(event_model.Event.products).join(product_model.Product.sales).filter(sale_model.Sale.unique_code == unique_code).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    acesso = validate_event_admin_access(db, current_user, db_event.id)
    if acesso not in ["admin", "commissioner"]:
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins and commissioners can check in sales")
    
    sale = db.query(sale_model.Sale).filter(sale_model.Sale.unique_code == unique_code).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    if sale.status == SaleStatus.CANCELED:
        raise HTTPException(status_code=400, detail="Sale is canceled and cannot be checked in")
    
    if sale.checked_at is not None:
        raise HTTPException(status_code=400, detail="Sale already checked in")

    sale.checked_at = datetime.utcnow()
    db.commit()
    db.refresh(sale)
    
    return sale

@router.put("/{id_sale}/cancel", response_model=sale_schema.Sale)
def cancel_sale(
    id_sale: int, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    db_event = db.query(event_model.Event).join(event_model.Event.products).join(product_model.Product.sales).filter(sale_model.Sale.id == id_sale).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event Not Found")

    acesso = validate_event_admin_access(db, current_user, db_event.id)

    if acesso != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can cancel sales")
    
    sale = db.query(sale_model.Sale).filter(sale_model.Sale.id == id_sale).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale Not Found")
    
    if sale.status == SaleStatus.CANCELED:
        raise HTTPException(status_code=400, detail="Sale already canceled")
    
    if sale.checked_at is not None:
        raise HTTPException(status_code=400, detail="Checked-in sales cannot be canceled")
    
    
    sale.status = SaleStatus.CANCELED
    sale.canceled_at = datetime.utcnow()
    db.commit()
    db.refresh(sale)
    
    return sale
