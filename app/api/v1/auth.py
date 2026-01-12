from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db, create_new_user
from app.core.dependencies import get_current_active_user
from app.models.users import User
from app.schemas.user import UserCreate
from app.services.user import UserService
from app.schemas.user import UserRead
from app.schemas.auth import UserLogin, Token
from app.core.security import verify_password, create_access_token


router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db_session=db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    try:
        new_user = UserService.create_user(db_session=db, user_data=user_in)
        db.commit()
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error") 


@router.post("/login" , response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    User = UserService.get_user_by_email(db_session=db, email=login_data.email)
    if not User or not verify_password(login_data.password, User.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(email=User.email)
    return {"access_token": access_token, "token_type": "bearer"}