from fastapi import FastAPI
from database import engine
from models import product_model
from routers import product_router

product_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    product_router.router,
    prefix="/products",
    tags=["Produtos"]
)

@app.get("/")
def read_root():
    return {"message": "API Uai-Festas no ar!"}