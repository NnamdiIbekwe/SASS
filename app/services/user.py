from app.models.users import User
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserService():
    @staticmethod
    def get_user_by_email(db_session: Session, email: str):
        return db_session.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db_session: Session, user_data: User):
        new_user = User(
            username=user_data['username'],
            email=user_data['email'],
            hashed_password=get_password_hash(user_data['password']),
            role=user_data.get('role', 'student')
        )
        db_session.add(new_user)
        db_session.flush()
        db_session.refresh(new_user)
        return new_user