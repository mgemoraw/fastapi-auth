from datetime import timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from deps import get_db
from models import Post, User
from schemas import PostCreate, PostResponse, UserCreate
from  sqlalchemy.orm import Session 

from utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_user, get_current_user, get_user_by_username, verify_token

router = APIRouter(
    prefix="/api/v1",
    tags = ["api"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
def greet():
    return {"message": "greetings"}


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username exists")
    return create_user(db=db, user=user)



@router.post("/registr")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username exists")
    return create_user(db=db, user=user)


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or passsword",
            headers={"WW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username}, expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verity-token/{totken}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}



@router.get("/auth/users")
async def get_users(user: user_dependency, db: Session=Depends(get_db)):
    if user:
        users = db.query(User).all()
        return users
    return {"users": []}


@router.post("/posts/post", response_model=None)
async def create_post(user: user_dependency, post: PostCreate, db:Session = Depends(get_db)):
    new_post = Post(content=post.content, user_id=post.user_id)
    db.add(new_post)
    db.commit()
    return {"post": post}


@router.get("/posts", response_model=List[PostResponse])
async def read_posts(user: user_dependency, db:Session=Depends(get_db)):
    posts = db.query(Post,).all()

    # query = db.query(User).join(User.posts,(User.id == Post.user_id))  
    # results = query.all() 
    
    return posts
