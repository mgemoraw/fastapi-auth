from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int 
    username: str 
    email: str 
  
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    user_id: int
    content: str
    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    id: int 
    user_id: int
    content: str 
    
    class Config:
        orm_mode = True 

