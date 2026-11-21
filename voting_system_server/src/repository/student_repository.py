from typing import Any

from ..database import Database
from .repository import Repository
from ..model import Student
from mariadb import Connection

class StudentRepository(Repository):
    ALLOWED_COLUMNS = {
        "student_name",
        "year"
    }

    def __init__(self, conn: Connection, db : Database):
        self._con = conn
        self._db = db

    def create(self, student: Student):
        cursor = self._con.cursor()
        try:
            cursor.execute("insert into students (student_name, year) values (?,?)", (student.student_name, student.year))
            return cursor.rowcount
        finally:
            cursor.close()

    def findAll(self):
        cursor = self._con.cursor()
        try:
            cursor.execute("select * from students")
            rows = self._db.fetchAll(cursor)
            students : list[Student] = self._db.hydrate(Student, rows)
            return students
        finally:
            cursor.close()

    def exists(self, student_name):
        cursor = self._con.cursor()
        try:
            cursor.execute("select * from students where student_name=(?)", (student_name,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def update(self, id, column: str, data: Any):
        if column not in self.ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {column}")

        cursor = self._con.cursor()
        try:
            cursor.execute(f"update students set {column}=(?) where student_id=(?)", (data, id,))
            if cursor.rowcount > 0:
                return True
            return False
        finally:
            cursor.close()

    def delete(self, id):
        cursor = self._con.cursor()
        try:
            cursor.execute("delete from students where student_id = (?)", (id,))
            return cursor.rowcount > 0
        finally:
            cursor.close()