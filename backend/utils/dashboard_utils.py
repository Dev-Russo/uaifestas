from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
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