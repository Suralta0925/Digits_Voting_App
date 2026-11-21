from ..database import Database
from mariadb import Connection

class ActiveElectionRepository:
    def __init__(self, conn: Connection):
        self._conn = conn

    def getActiveElection(self):
        cursor = self._conn.cursor()
        try:
            cursor.execute("select election_id from active_election where id=1")
            row = cursor.fetchone()
            if row is None: return None
            return row[0]
        finally:
            cursor.close()

    def setActiveElection(self, election_id):
        cursor = self._conn.cursor()
        try:
            cursor.execute("insert into active_election (election_id) values (?)", (election_id,))
            return cursor.rowcount > 0
        finally:
            cursor.close()

    def clearActiveElection(self):
        if self.getActiveElection() is not None:
            cursor = self._conn.cursor()
            try:
                cursor.execute("delete from active_election where id = 1")
                return True
            finally:
                cursor.close()
        return False