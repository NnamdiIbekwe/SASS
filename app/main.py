from fastapi import FastAPI
import os
from dotenv import load_dotenv
from app.schemas.user import UserCreate
from app.database.base import get_db

load_dotenv()



app = FastAPI(title="Student Assignment Submission System")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Assignment Submission System!"}

@app.post("/students/register", status_code=201)
async def register_student(student: UserCreate):

    # Logic to register a student
    return {"message": "Student registered successfully", "student": student}

@app.post("/teachers/register")
async def register_teacher(teacher: dict):
    # Logic to register a teacher
    return {"message": "Teacher registered successfully", "teacher": teacher}

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    # Logic to get student details
    return {"student_id": student_id, "username": username}

@app.get("/teachers/{teacher_id}")
async def get_teacher(teacher_id: int):
    # Logic to get teacher details
    return {"teacher_id": teacher_id, "username": username}

@app.patch("users/me")
async def update_user_profile(user_updates: dict):
    # Logic to update user profile
    return {"message": "User profile updated successfully", "updates": user_updates}

@app.post("/assignments/submit")
async def submit_assignment(assignment: dict):
    # Logic to submit an assignment
    return {"message": "Assignment submitted successfully", "assignment": assignment}

@app.get("/assignments/")
async def list_assignments():
    # Logic to list all assignments
    return {"assignments": []}

@app.get("assignments/mine")
async def list_my_assignments():
    # Logic to list assignments for the logged-in user
    return {"my_assignments": []}
@app.get("/assignments/{assignment_id}")
async def get_assignment(assignment_id: int):
    # Logic to get assignment details
    return {"assignment_id": assignment_id, "details": "Assignment details here"}

@app.patch("/assignments/{assignment_id}")
async def update_assignment(assignment_id: int, updates: dict):
    # Logic to update assignment details
    return {"message": "Assignment updated successfully", "assignment_id": assignment_id, "updates": updates}

@app.post("/assignments/{assignment_id}/comment")
async def add_comment(assignment_id: int, comment: dict):
    # Logic to add a comment to an assignment
    return {"message": "Comment added successfully", "assignment_id": assignment_id, "comment": comment}

@app.post("/assignments/{assignment_id}/grade")
async def grade_assignment(assignment_id: int, grade: dict):
    # Logic to grade an assignment
    return {"message": "Assignment graded successfully", "assignment_id": assignment_id, "grade": grade}

@app.patch("/assignments/{assignment_id}/status")
async def update_assignment_status(assignment_id: int, status: dict):
    # Logic to update assignment status
    return {"message": "Assignment status updated successfully", "assignment_id": assignment_id, "status": status}


print(os.getenv("DATABASE_URL"))