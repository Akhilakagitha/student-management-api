from sqlalchemy.orm import Session
from models import Student
from schema import StudentCreate


# CREATE
def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        name=student.name,
        age=student.age,
        email=student.email,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# READ - all students
def get_students(db: Session):
    return db.query(Student).all()


# READ - one student
def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


# UPDATE
def update_student(db: Session, student_id: int, student_data: StudentCreate):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        student.name = student_data.name
        student.age = student_data.age
        student.email = student_data.email
        student.course = student_data.course

        db.commit()
        db.refresh(student)

    return student


# DELETE
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student:
        db.delete(student)
        db.commit()

    return student