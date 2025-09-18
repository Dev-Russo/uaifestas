from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import user_schema
from models import user_model
from dependencies import get_db
from utils import password_utils

router = APIRouter()

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já Registrado")
    
    hash_pass = password_utils.hash_password(user.password)
    
    new_user = user_model.User(
        email = user.email,
        username = user.username,
        hashed_password = hash_pass,
        role = user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/", response_model=list[user_schema.User])
def get_users(db: Session = Depends(get_db)):
    db_users = db.query(user_model.User).all()
    return db_users