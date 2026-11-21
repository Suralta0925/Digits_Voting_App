from database import Database
from mariadb import Connection
from .active_election_repository import ActiveElectionRepository
from datetime import datetime, time
class AttendanceRepository:

    def __init__(self, conn: Connection, db: Database):
        self._conn = conn
        self.db = db

    def record(self, student_id):
        election_id = ActiveElectionRepository(self._conn).getActiveElection()
        now = datetime.now().time()
        cursor = self._conn.cursor()
        try:
            cursor.execute("insert into attendance (election_id, student_id, checked_in_at) values (?,?,?)",(election_id,student_id, now))
            return cursor.rowcount > 0
        finally:
            cursor.close()
    def getPresent(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute("select s.student_name from attendance a inner join students s on s.student_id = a.student_id")
            rows = self.db.fetchAll(cursor)
            return rows[0]
        finally:
            cursor.close()

    def provideTickets(self):
        # TODO: Provide tickets aka credential for each position
        pass
