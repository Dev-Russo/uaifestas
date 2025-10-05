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
    
    if current_user.role != "admin" and current_user not in event.administrators and current_user not in event.commissioners:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    stats = get_statistics(db, event_id, start_date.date(), end_date.date(), current_user)
    
    # Get additional event statistics
    total_products = db.query(func.count(product_model.Product.id)).filter(
        product_model.Product.event_id == event_id
    ).scalar()
    
    total_sellers = db.query(func.count(func.distinct(sale_model.Sale.seller_id))).filter(
        sale_model.Sale.product_id.in_(
            db.query(product_model.Product.id).filter(product_model.Product.event_id == event_id)
        )
    ).scalar()
    
    # Calculate sales metrics for the period
    paid_sales = stats["total_sales"]
    canceled_sales = stats["total_canceled"]
    total_revenue = stats["total_revenue"]
    
    # Calculate growth percentages (simplified - would need previous period data)
    sales_growth_percentage = None  # Would need to implement comparison with previous period
    revenue_growth_percentage = None  # Would need to implement comparison with previous period
    
    sales_metrics = dashboard_schema.SaleMetrics(
        total_sales=paid_sales + canceled_sales,
        total_revenue=total_revenue,
        average_ticket=stats["avg_sale_value"],
        paid_sales=paid_sales,
        canceled_sales=canceled_sales,
        today_sales=0,  # Would need to implement daily calculations
        today_revenue=0.0,  # Would need to implement daily calculations
        week_sales=0,  # Would need to implement weekly calculations
        week_revenue=0.0,  # Would need to implement weekly calculations
        month_sales=paid_sales,  # Using current period as month
        month_revenue=total_revenue,  # Using current period as month
        sales_growth_percentage=sales_growth_percentage,
        revenue_growth_percentage=revenue_growth_percentage
    )
    
    dashboard = dashboard_schema.EventDashboard(
        event_id=event.id,
        event_name=event.name,
        event_status=event.status,
        event_date=event.event_date,
        created=event.created,
        sales_metrics=sales_metrics,
        product_stats=[],  # Would need to implement product statistics
        seller_stats=[],  # Would need to implement seller statistics
        top_products=[],  # Would need to implement top products
        analysis_period_days=str(days)
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