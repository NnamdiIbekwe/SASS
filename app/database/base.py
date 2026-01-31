import os
from fastapi import Depends
# from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine
from passlib.context import CryptContext
import bcrypt
from app.schemas.user import UserCreate
from app.database.session import SessionLocal
# from sqlalchemy.orm import Session
# from app.models import *

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

salt = bcrypt.gensalt()

response = {"message": "User created"}


def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, password=user.hashed_password)
    db_user.hashed_password = bcrypt.hashpw(user_updates.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.add(new_user)
    db.commit() 
    db.refresh(new_user) 
 
    return new_user

    