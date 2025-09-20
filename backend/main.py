from fastapi import FastAPI
from database import engine
<<<<<<< HEAD
from models import product_model
from routers import product_router

product_model.Base.metadata.create_all(bind=engine)
=======
from routers import product_route, event_route, user_route, auth_route, sale_route
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1

app = FastAPI()

app.include_router(
<<<<<<< HEAD
    product_router.router,
=======
    product_route.router,
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1
    prefix="/products",
    tags=["Produtos"]
)

<<<<<<< HEAD
@app.get("/")
def read_root():
    return {"message": "API Uai-Festas no ar!"}
=======
app.include_router(
    event_route.router,
    prefix="/events",
    tags=["Eventos"]
)

app.include_router(
    user_route.router,
    prefix="/user",
    tags=["Usuarios"]
)

app.include_router(
    auth_route.router,
    prefix="/login",
    tags=["Authentication"]
)

app.include_router(
    sale_route.router,
    prefix="/sale",
    tags=["Vendas"]
)

@app.get("/")
def read_root():
    return {"message": "API UaiFestas no ar!"}
>>>>>>> 96eeea13e24f9e544c58150cf9ae72d1417c78a1
