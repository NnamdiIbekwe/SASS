from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db, create_new_user
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.core.security import get_password_hash



router = APIRouter(
    prefix="/users",
    tags=["users"],
)   


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = (
        db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    )
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username or email already registered"
        )

    new_user = create_new_user(user, db)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_updates: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    if user_updates.email:
        email_exists = db.query(User).filter(User.email == user_updates.email, User.id != user_id).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        db_user.email = user_updates.email

    if user_updates.password:
        db_user.hashed_password = get_password_hash(user_updates.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user