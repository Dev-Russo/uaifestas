from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    
class UserCreate(UserBase):
    password: str
    role: str
    
class User(UserBase):
    id: int
    role: str
    
    class Config:
        from_attributes = True