from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, get_db
import models
import crud
import schema


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


@app.post("/students", response_model=schema.StudentResponse)
def create_student(
    student: schema.StudentCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_student(db, student)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )


@app.get("/students", response_model=list[schema.StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put(
    "/students/{student_id}",
    response_model=schema.StudentResponse
)
def update_student(
    student_id: int,
    student: schema.StudentCreate,
    db: Session = Depends(get_db)
):
    updated_student = crud.update_student(db, student_id, student)

    if not updated_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return updated_student

@app.delete(
    "/students/{student_id}",
    response_model=schema.StudentResponse
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    deleted_student = crud.delete_student(db, student_id)

    if not deleted_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return deleted_student