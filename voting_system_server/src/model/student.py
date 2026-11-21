from pydantic import BaseModel

class Student(BaseModel):
    student_id: int | None
    student_name: str
    year: int