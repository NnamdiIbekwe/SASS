from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from datetime import datetime
from app.database.base import Base
from datetime import datetime
from app.schemas.assignment import AssignmentStatus





class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=False)
    status = Column(String, default=AssignmentStatus.PENDING)
    score = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)