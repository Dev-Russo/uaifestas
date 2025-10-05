from fastapi import FastAPI
from database import engine
from routers import product_route, event_route, user_route, auth_route, sale_route, dashboard_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.18.5:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

app.include_router(
    sale_route.router,
    prefix="/sale",
    tags=["Vendas"]
)

app.include_router(
    dashboard_route.router,
    prefix="/dashboard",
    tags=["Dashboard"]
)
    

@app.get("/")
def read_root():
    return {"message": "API UaiFestas no ar!"}
