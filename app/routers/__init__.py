from .v1 import jobs, auth
from fastapi import APIRouter
from .v1.exceptions import setup_exception_handlers
api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])

