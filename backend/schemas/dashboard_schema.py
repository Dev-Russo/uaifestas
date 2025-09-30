from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
    
class SaleMetrics(BaseModel):
    total_sales: int
    total_revenue: float
    average_ticket: float
    paid_sales: int
    canceled_sales: int
    
    today_sales: int
    today_revenue: float
    week_sales: int
    week_revenue: float
    month_sales: int
    month_revenue: float
    
    sales_growth_percentage: float | None = None
    revenue_growth_percentage: float | None = None
    
class ProductSalesStats(BaseModel):
    product_id: int
    product_name: str
    total_sales: int
    total_revenue: float
    average_ticket: float
    percentage_of_sales: float         # % do total de vendas
    percentage_of_revenue: float       # % da receita total
    
    stock_remaining: Optional[int]  # Se aplicável
    stock_sold: Optional[int]       # Se aplicável


class SallerStats(BaseModel):
    seller_id: int
    seller_name: str
    total_sales: int
    total_revenue: float
    average_ticket: float
    percentage_of_sales: float         # % do total de vendas
    percentage_of_revenue: float       # % da receita total

    sales_by_product: int              # Quantidade por produto
    
class EventDashboard(BaseModel):
    event_id: int
    event_name: str
    event_status: str
    event_date: Optional[datetime]
    created: datetime
    
    sales_metrics: SaleMetrics
    
    product_stats: List[ProductSalesStats] = Field(default_factory=list)
    seller_stats: List[SallerStats] = Field(default_factory=list)
    
    top_products: List[ProductSalesStats] = Field(default_factory=list)
    
    analysis_period_days: Optional[str]
    
    
class EventSummary(BaseModel):
    event_id: int
    event_name: str
    event_status: str
    event_date: Optional[datetime]
    created: datetime
    image_url: Optional[str] = None
    
    total_products: int
    total_sellers: int
    total_sales: int
    total_revenue: float
    
    average_ticket: float
    
    last_sale_date: Optional[datetime]
    last_cancellation_date: Optional[datetime]