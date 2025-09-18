from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user_model import User as UserModel
from dependencies import get_db
from utils.password_utils import verify_password 
from utils.auth_utils import create_access_token   
from schemas.token_schema import Token

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data = {
            "sub": user.username,
            "role": user.role
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
