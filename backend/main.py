from fastapi import FastAPI
from database import engine
from routers import product_route, event_route, user_route, auth_route

app = FastAPI()

app.include_router(
    product_route.router,
    prefix="/products",
    tags=["Produtos"]
)

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

@app.get("/")
def read_root():
    return {"message": "API UaiFestas no ar!"}