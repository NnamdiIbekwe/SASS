import os
from dotenv import load_dotenv

load_dotenv()

import logging
from fastapi import FastAPI, Depends, HTTPException
from app.schemas.user import UserCreate
from app.database.base import get_db
from app.api.v1 import auth
from app.core.config import settings
from sqlalchemy.orm import Session
from app.models.users import User as Student


logger=logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


app = FastAPI(title="Student Assignment Submission System")

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])




@app.post("/students/register", status_code=201)
async def register_student(student: UserCreate, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(Student.email == student.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(student.password)

    new_student = Student(
        name=student.name,
        email=student.email,
        password=hashed_password
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student registered successfully",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email
        }
    }

    return {"message": "Student registered successfully", "student": student}

@app.post("/teachers/register")
async def register_teacher(teacher: dict):

    return {"message": "Teacher registered successfully", "teacher": teacher}

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    return {"student_id": student_id, "username": username}

@app.get("/teachers/{teacher_id}")
async def get_teacher(teacher_id: int):
    return {"teacher_id": teacher_id, "username": username}

@app.patch("/users/me")
async def update_user_profile(user_updates: dict):
    return {"message": "User profile updated successfully", "updates": user_updates}

@app.post("/assignments/submit")
async def submit_assignment(assignment: dict):
    return {"message": "Assignment submitted successfully", "assignment": assignment}

@app.get("/assignments/")
async def list_assignments():
    return {"assignments": []}

@app.get("/assignments/mine")
async def list_my_assignments():
    return {"my_assignments": []}

@app.get("/assignments/{assignment_id}")
async def get_assignment(assignment_id: int):
    return {"assignment_id": assignment_id, "details": "Assignment details here"}

@app.patch("/assignments/{assignment_id}")
async def update_assignment(assignment_id: int, updates: dict):
    return {"message": "Assignment updated successfully", "assignment_id": assignment_id, "updates": updates}

@app.post("/assignments/{assignment_id}/comment")
async def add_comment(assignment_id: int, comment: dict):
    return {"message": "Comment added successfully", "assignment_id": assignment_id, "comment": comment}

@app.post("/assignments/{assignment_id}/grade")
async def grade_assignment(assignment_id: int, grade: dict):
    return {"message": "Assignment graded successfully", "assignment_id": assignment_id, "grade": grade}

@app.patch("/assignments/{assignment_id}/status")
async def update_assignment_status(assignment_id: int, status: dict):
    return {"message": "Assignment status updated successfully", "assignment_id": assignment_id, "status": status}


print(os.getenv("DATABASE_URL"))