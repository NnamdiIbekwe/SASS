from sqlalchemy import Boolean, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base
from app.schemas.user import UserRole



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(70), unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.STUDENT)
    assignments = relationship("Assignment", back_populates="student")
    created_at = Column(DateTime, default=datetime.utcnow)



    