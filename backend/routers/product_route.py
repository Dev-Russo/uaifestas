from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import user_model, product_model
from schemas import product_schema
from dependencies import get_db
from utils.auth_utils import get_current_user
from utils.product_utils import check_admin_permission_for_event 

router = APIRouter()

@router.post("/", response_model=product_schema.Product)
def create_product(
    event_id: int,
    product: product_schema.ProductCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    check_admin_permission_for_event(db, current_user, event_id)

    db_product = product_model.Product(**product.dict(), event_id=event_id)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@router.get("/", response_model=list[product_schema.Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(product_model.Product).all()
    return products

@router.get("/{id_product}", response_model=product_schema.Product)
def get_by_id(id_product: int, db: Session = Depends(get_db)):
    product = db.query(product_model.Product).filter(product_model.Product.id == id_product).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{id_product}", response_model=product_schema.Product)
def update_by_id(
    id_product: int,
    product: product_schema.ProductBase,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == id_product).first()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not Found")

    check_admin_permission_for_event(db, current_user, db_product.event_id)

    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete("/{id_product}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    id_product: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == id_product).first()
    
    if db_product:
        check_admin_permission_for_event(db, current_user, db_product.event_id)
        
        db.delete(db_product)
        db.commit()
    
    return {"message": f"Item with {id_product} deleted successfully"}