from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class Student(BaseModel):
    name: str
    roll: int
    CGPA: float

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    roll: Optional[int] = None
    CGPA: Optional[float] = None

students = {
    1: {
        "name": "Johan Dew",
        "roll": 20,
        "CGPA": 3.55
    },
    2: {
        "name": "Mark",
        "roll": 22,
        "CGPA": 3.05
    }
}


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0, lt=4)):
    return students.get(student_id, {"error": "Student not found"})

@app.get("/get-by-name")
def get_student_by_name(name: Optional[str] = Query(None, description="Name of the student")):
    for student_id, student in students.items():
        if student["name"] == name:
            return student
    return {"Data": "Not Found"}

@app.get("/get-by-name-and-id/{student_id}")
def get_student_by_name_and_id(name: Optional[str] = Query(None, description="Name of the student"), student_id : int = Path(..., description="The ID of the student you want to view")):
    for student_id, student in students.items():
        if student["name"] == name:
            return student
    return {"Data": "Not Found"}

@app.post("/create-student/{student_id}")
def create__new_student(student_id: int, student: Student):
    if student_id in students:
        return "Error: Student exists"
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student dosen't exists"}
    if student.name != None:
        students[student_id].name = student.name
    if student.roll != None:
        students[student_id].roll = student.roll
    if student.CGPA != None:
        students[student_id].CGPA = student.CGPA

    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {"Error": "Student dose't exists"}
    del students[student_id]
    return {"Message": "Student Deleted successfully!"}