import os
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(prefix="/assignments", tags=["Assignments"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def submit_assignment(
    student_name: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(username=student_name).first()
    if not user:
        return {"error": "Student not found"}

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    assignment = models.Assignment(
        subject=subject,
        description=description,
        file_path=file_path,
        student_id=user.id
    )
    db.add(assignment)
    db.commit()
    return {"message": "Assignment submitted"}

@router.get("/")
def list_assignments(db: Session = Depends(get_db)):
    return db.query(models.Assignment).all()

@router.get("/user/{student_name}")
def list_student_assignments(student_name: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username=student_name).first()
    if not user:
        return {"error": "Student not found"}
    return db.query(models.Assignment).filter_by(student_id=user.id).all()

@router.post("/{assignment_id}/comment")
def add_comment(
    assignment_id: int,
    commenter_name: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    assignment = db.query(models.Assignment).filter_by(id=assignment_id).first()
    if not assignment:
        return {"error": "Assignment not found"}

    comment = models.Comment(
        assignment_id=assignment_id,
        commenter_name=commenter_name,
        content=content
    )
    db.add(comment)
    db.commit()
    return {"message": "Comment added"}
