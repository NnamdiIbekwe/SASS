from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database.base import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user import UserService
from app.schemas.auth import UserLogin, Token
from app.core.security import verify_password, create_access_token


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(
        db_session=db, 
        email=user_in.email
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    try:
        new_user = UserService.create_user(db_session=db, user_data=user_in)
        db.commit()
        db.refresh(new_user)
        return db_user
    except Exception as e:
        db.rollback()
        logger.exception("unexpected error during user signup")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Internal Server Error"
        ) from e


@router.post("/login" , response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db_session=db, email=login_data.email)
   
    if not db_user or not verify_password(login_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )

    access_token = create_access_token(email=db_user.email)
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }
