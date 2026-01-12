from app.database.session import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from fastapi import Depends, HTTPException
from app.core.security import decode_access_token
from app.models.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = decode_access_token(token)
    if data is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    user_id = db.query(user).filter(user.email == data.get('sub')).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 