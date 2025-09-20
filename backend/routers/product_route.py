from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models import product_model
from schemas import product_schema

router = APIRouter()

@router.post("/", response_model=product_schema.Product)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
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
    product =  db.query(product_model.Product).filter(product_model.Product.id_product == id_product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Products not found")
    return product

@router.put("/{id_product}")
def update_by_id(id_product: int, product: product_schema.ProductBase ,db: Session = Depends(get_db)):
    db_product = db.query(product_model.Product).filter(product_model.Product.id_product == id_product).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not Found")
    
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
def delete_by_id(id_product: int, db : Session = Depends(get_db)):
    product = db.get(product_model.Product, id_product)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Item with {id_product} deleted sucessfully"}