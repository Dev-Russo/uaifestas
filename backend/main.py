from fastapi import FastAPI
from database import engine
from models import product_model
from routers import product_route

app = FastAPI()

app.include_router(
    product_route.router,
    prefix="/products",
    tags=["Produtos"]
)

@app.get("/")
def read_root():
    return {"message": "API UaiFestas no ar!"}