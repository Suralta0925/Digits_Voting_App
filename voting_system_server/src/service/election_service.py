from repository import ActiveElectionRepository
from ..database import Database
from ..repository import ElectionRepository
from ..repository import Repository
from .service_response import ServiceResponse
from datetime import datetime, time

class ElectionService:

    def __init__(self, db: Database):
        self.db : Database = db

    def createElection(self, title):
        with self.db.transaction() as conn:
            repo = ElectionRepository(conn, self.db)
            if not repo.exists(title):
                repo.create(title)
                return ServiceResponse(
                    success=True,
                    message=f"Successfully created {title} election.",
                ).to_dict()
            return ServiceResponse(
                success=False,
                message=f"Election title \"{title}\" already exists."
            ).to_dict()
    def getAllElection(self):
        with self.db.transaction() as conn:
            repo = ElectionRepository(conn, self.db)
            return ServiceResponse(
                success=True,
                message= "Success!",
                data= repo.findAll()
            ).to_dict()

    def deleteElection(self, id):
        with self.db.transaction() as conn:
            repo = ElectionRepository(conn, self.db)
            if repo.delete(id):
                return ServiceResponse(success=True, message="Successfully Deleted!").to_dict()
            return ServiceResponse(success=False, message="Failed to delete: id doesn't exists.").to_dict()
    def start(self, id):
        with self.db.transaction() as conn:
            repo: Repository = ElectionRepository(conn, self.db)
            now = datetime.now()
            active_election = ActiveElectionRepository(conn)
            if active_election.getActiveElection() is None:
                active_election.setActiveElection(id)
                repo.update(id, "start_time", now.time())
                repo.update(id, "start_at", now.date())
                return ServiceResponse(
                    success=True,
                    message=f"Election started."
                )
            else:
                return ServiceResponse(
                    success=False,
                    message=f"An Instance of an election is currently running."
                )



