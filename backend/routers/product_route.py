from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from backend.models import event_model
from models import user_model
from utils.auth_utils import get_current_user
from dependencies import get_db
from models import product_model
from schemas import product_schema

router = APIRouter()

@router.post("/", response_model=product_schema.Product)
def create_product(
    product: product_schema.ProductCreate, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can create products")
    if product.event_id is not None:
        event = db.query(event_model.Event).filter(event_model.Event.id == product.event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event Not Found")
        if event.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Operation not permitted: you can only add products to your own events")
    
    db_product = product_model.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[product_schema.Product])
def get_all_products(db: Session = Depends(get_db)):
    product =  db.query(product_model.Product).all()
    return product

@router.get("/{id_product}", response_model=product_schema.Product)
def get_by_id(id_product: int, db: Session = Depends(get_db)):
    product =  db.query(product_model.Product).filter(product_model.Product.id == id_product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Products not found")
    return product

@router.put("/{id_product}")
def update_by_id(
    id_product: int, 
    product: product_schema.ProductBase, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can update products")

    db_product = db.query(product_model.Product).options(joinedload(product_model.Product.event)).filter(product_model.Product.id == id_product).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not Found")
    
    if db_product.event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only update products of your own events")
    
    if product.name_product is not None:
        db_product.name_product = product.name_product
    if product.description_product is not None:
        db_product.description_product = product.description_product
    if product.price is not None:
        db_product.price = product.price
        
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete("/{id_product}")
def delete_by_id(
    id_product: int, 
    db : Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can delete products")
    
    product = db.get(product_model.Product, id_product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only delete products of your own events")
    
    db.delete(product)
    db.commit()
    return {"message": f"Item with {id_product} deleted sucessfully"}