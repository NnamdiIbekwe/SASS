from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate
from app.database.base import create_new_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)   
@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    new_user = create_new_user(user, db)
    return new_user

@router.patch("/{user_id}", response_model=UserUpdate)
def update_user(user_id: int, user_updates: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_updates.email:
        db_user.email = user_updates.email
    if user_updates.password:
        db_user.hashed_password = bcrypt.hashpw(user_updates.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    db.commit()
    db.refresh(db_user)
    return db_user