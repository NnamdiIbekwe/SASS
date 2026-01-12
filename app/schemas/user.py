from pydantic import BaseModel, EmailStr, ConfigDict
import enum
# from sqlalchemy import Enum as SqlEnum

class UserRole(str, enum.Enum):
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None  = None
    password: str | None = None

class UserRead(UserBase):
    id: int
    created_at: str

    class Config:
        model_config = ConfigDict(from_attributes=True)
