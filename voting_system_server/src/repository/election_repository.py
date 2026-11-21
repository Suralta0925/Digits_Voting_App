from mariadb import Connection

from ..database import Database
from ..model import Election
from ..repository.repository import Repository


class ElectionRepository(Repository):

    ALLOWED_COLUMNS = {
        'election_name',
        'start_time',
        'end_time',
        'status',
        'start_at'
    }


    def __init__(self, conn: Connection, db : Database):
        self._conn = conn
        self.db: Database = db

    def create(self, title: str):
        cursor = self._conn.cursor()
        try:
            cursor.execute("""
                       insert into elections (election_name) values (?)
                       """, (title,))
            res = cursor.rowcount
            return res
        finally:
            cursor.close()

    def exists(self, params):
        cursor = self._conn.cursor()
        try:
            cursor.execute("select * from elections where election_name= (?) ", (params,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()


    def findById(self, id) -> 'Election':
        cursor = self._conn.cursor()
        try:
            cursor.execute("select * where election_id = (?)",(id,))
            rows = self.db.fetchAll(cursor)
            res : Election = self.db.hydrate(Election, rows)
            return res
        finally:
            cursor.close()

    def findAll(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute("select * from elections")
            rows = self.db.fetchAll(cursor)
            res : list[Election] = self.db.hydrate(Election, rows)
            return res
        finally:
            cursor.close()

    def update(self, id : int, column ,data: str):
        if column not in self.ALLOWED_COLUMNS:
            raise ValueError(f"Invalid column: {column}")
        cursor = self._conn.cursor()
        try:
            cursor.execute(f"update elections set {column}=(?) where election_id= (?)", (column,data, id,))
            return cursor.rowcount > 0
        finally:
            cursor.close()


    def delete(self, id):
        cursor = self._conn.cursor()
        try:
            cursor.execute("delete from elections where election_id = (?)", (id,))
            return cursor.rowcount > 0
        finally:
            cursor.close()
