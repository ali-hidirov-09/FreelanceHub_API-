from .v1 import jobs
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
