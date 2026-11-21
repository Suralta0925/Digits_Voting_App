from fastapi import APIRouter

from ..database import Database
from ..model import Election
from ..service import ElectionService

election_router = APIRouter()
db = Database()
service = ElectionService(db)

@election_router.post('/create')
def createElection(election: Election):
    return service.createElection(election.title)

@election_router.get('/get')
def getElection():
    return service.getAllElection()

@election_router.delete('/delete')
def deleteElection(id):
    return service.deleteElection(id)