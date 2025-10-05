from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import case, func, and_, desc
from datetime import datetime, timedelta, date
from typing import Optional, List
from dependencies import get_db
from utils.auth_utils import get_current_user
from models import user_model, event_model, sale_model, product_model
from schemas import dashboard_schema
from enums import SaleStatus, EventStatus


def get_statistics(db: Session, event_id: int, start_date: date, end_date: date, current_user: user_model.User):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    if current_user.role != "admin" and current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    total_sales = db.query(func.count(sale_model.Sale.id)).join(product_model.Product).filter(
        product_model.Product.event_id == event_id,
        sale_model.Sale.status == SaleStatus.PAID,
        sale_model.Sale.created_at >= start_date,
        sale_model.Sale.created_at <= end_date
    ).scalar()

    total_revenue = db.query(func.coalesce(func.sum(product_model.Product.price), 0)).join(sale_model.Sale).filter(
        product_model.Product.event_id == event_id,
        sale_model.Sale.status == SaleStatus.PAID,
        sale_model.Sale.created_at >= start_date,
        sale_model.Sale.created_at <= end_date
    ).scalar()

    avg_sale_value = total_revenue / total_sales if total_sales > 0 else 0.0

    total_canceled = db.query(func.count(sale_model.Sale.id)).join(product_model.Product).filter(
        product_model.Product.event_id == event_id,
        sale_model.Sale.status == SaleStatus.CANCELED,
        sale_model.Sale.created_at >= start_date,
        sale_model.Sale.created_at <= end_date
    ).scalar()

    cancellation_rate = (total_canceled / (total_sales + total_canceled) * 100) if (total_sales + total_canceled) > 0 else 0.0

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "avg_sale_value": avg_sale_value,
        "total_canceled": total_canceled,
        "cancellation_rate": cancellation_rate
    }
    
def get_sellers_statistics(
    db: Session,
    event_id: int,
    start_date: date,
    end_date: date,
    current_user: user_model.User,
    seller_id: Optional[int] = None
):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    if current_user.role != "admin" and current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    query = db.query(
        user_model.User.id.label("seller_id"),
        user_model.User.name.label("seller_name"),
        func.count(sale_model.Sale.id).label("total_sales"),
        func.coalesce(func.sum(product_model.Product.price), 0).label("total_revenue"),
        func.coalesce(func.sum(
            case([(sale_model.Sale.status == SaleStatus.CANCELED, product_model.Product.price)], else_=0)
        ), 0).label("total_canceled")
    ).join(sale_model.Sale, sale_model.Sale.seller_id == user_model.User.id
    ).join(product_model.Product, sale_model.Sale.product_id == product_model.Product.id
    ).filter(
        product_model.Product.event_id == event_id,
        sale_model.Sale.created_at >= start_date,
        sale_model.Sale.created_at <= end_date
    ).group_by(user_model.User.id)

    if seller_id:
        query = query.filter(user_model.User.id == seller_id)

    sellers_stats = []
    for row in query.all():
        cancellation_rate = (row.total_canceled / (row.total_sales + row.total_canceled) * 100) if (row.total_sales + row.total_canceled) > 0 else 0.0
        sellers_stats.append(dashboard_schema.SallerStats(
            seller_id=row.seller_id,
            seller_name=row.seller_name,
            total_sales=row.total_sales,
            total_revenue=row.total_revenue,
            total_canceled=row.total_canceled,
            cancellation_rate=cancellation_rate
        ))

    return sellers_stats