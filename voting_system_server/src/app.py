from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from .route import election_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:8080"
)
app.include_router(election_router, prefix="/api/v1/election")
