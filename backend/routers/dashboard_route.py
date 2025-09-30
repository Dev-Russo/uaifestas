from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta, date
from typing import Optional, List
from dependencies import get_db
from utils.auth_utils import get_current_user
from utils.dashboard_utils import get_sellers_statistics, get_statistics
from models import user_model, event_model, sale_model, product_model
from schemas import dashboard_schema
from enums import SaleStatus, EventStatus

router = APIRouter()

@router.get("/event/{event_id}", response_model=dashboard_schema.EventDashboard)
def get_event_dashboard(
    event_id: int,
    days: Optional[int] = Query(30, description="Período de análise em dias"),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    if current_user.role != "admin" or current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    stats = get_statistics(db, event_id, start_date.date(), end_date.date(), current_user)
    
    
    dashboard = dashboard_schema.EventDashboard(
        total_sales=stats["total_sales"],
        total_revenue=stats["total_revenue"],
        avg_sale_value=stats["avg_sale_value"],
        total_products=stats["total_products"]
    )
    
    return dashboard

@router.get("/event/{event_id}/sales-metrics", response_model=dashboard_schema.SaleMetrics)
def get_sales_metrics(
    event_id: int,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")
    
    if current_user.role != "admin" or current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    if not start_date:
        start_date = datetime.utcnow().date() - timedelta(days=30)
    
    if not end_date:
        end_date = datetime.utcnow().date()
        
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")
    
    stats = get_statistics(db, event_id, start_date, end_date, current_user)

    cancellation_rate = (stats["total_canceled"] / (stats["total_sales"] + stats["total_canceled"]) * 100) if (stats["total_sales"] + stats["total_canceled"]) > 0 else 0.0
    
    total_sales = stats["total_sales"]
        
    metrics = dashboard_schema.SaleMetrics(
        total_sales=total_sales,
        total_revenue=stats["total_revenue"],
        avg_sale_value=stats["avg_sale_value"],
        total_canceled=stats["total_canceled"],
        cancellation_rate=cancellation_rate
    )
    
    return metrics

@router.get("/event/{event_id}/products", response_model=List[dashboard_schema.ProductSalesStats])
def get_products_stats(
    event_id: int,
    limit: Optional[int] = Query(None, description="Limitar quantidade de produtos"),
    order_by: str = Query("sales", description="Ordenar por: sales, revenue"),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")

    if current_user.role != "admin" or current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    products = db.query(product_model.Product).filter(product_model.Product.event_id == event_id)

    if order_by == "revenue":
        products = products.join(sale_model.Sale).filter(sale_model.Sale.status == SaleStatus.PAID).group_by(product_model.Product.id).order_by(func.sum(product_model.Product.price).desc())
    else:
        products = products.join(sale_model.Sale).filter(sale_model.Sale.status == SaleStatus.PAID).group_by(product_model.Product.id).order_by(func.count(sale_model.Sale.id).desc())

    if limit:
        products = products.limit(limit)

    return products.all()

@router.get("/event/{event_id}/sellers", response_model=List[dashboard_schema.SallerStats])
def get_sellers_stats(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    event = db.query(event_model.Event).filter(event_model.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event Not Found")

    if current_user.role != "admin" or current_user not in event.administrators:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    sellers_stats = get_sellers_statistics(db, event_id, datetime.utcnow().date() - timedelta(days=30), datetime.utcnow().date(), current_user)
    
    return sellers_stats