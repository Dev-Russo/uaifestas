from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.auth_utils import get_current_user
from schemas import user_schema, event_schema
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

@router.get("/{id_user}", response_model=user_schema.User)
def get_user_by_id(id_user: int, db: Session = Depends(get_db)):
    db_user = db.get(user_model.User, id_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user

@router.get("/{id_user}/events", response_model=list[event_schema.Event])
def get_events_user(id_user: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user.events

@router.put("/{id_user}", response_model=user_schema.User)
def update_user(
    id_user: int, 
    user: user_schema.UserCreate, 
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    db_user = db.get(user_model.User, id_user)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    if current_user.id != db_user.id and current_user.role != "client":
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only update your own user")
    elif current_user.role != "admin" and db_user.role != "commissioner":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can update commissioners")
    
    if user.email != db_user.email:
        email_exists = db.query(user_model.User).filter(user_model.User.email == user.email).first()
        if email_exists:
            raise HTTPException(status_code=400, detail="Email já Registrado")
    elif user.email is not None:   
        db_user.email = user.email

    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.hashed_password = password_utils.hash_password(user.password)
    if user.role is not None:
        db_user.role = user.role

    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/{id_user}")
def delete_user(
    id_user: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
    ):
    db_user = db.get(user_model.User, id_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    if current_user.id != db_user.id and current_user.role != "client":
        raise HTTPException(status_code=403, detail="Operation not permitted: you can only update your own user")
    elif current_user.role != "admin" and db_user.role != "commissioner":
        raise HTTPException(status_code=403, detail="Operation not permitted: only admins can update commissioners")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User with {id_user} deleted sucessfully"}