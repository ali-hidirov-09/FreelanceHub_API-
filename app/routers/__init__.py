from .v1 import jobs, auth, applications, uploads, freelancers, admin, ws
from fastapi import APIRouter
from .v1.exceptions import setup_exception_handlers
api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
# api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
# api_router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])
# api_router.include_router(freelancers.router, prefix="/freelancers", tags=["Freelancers"])
# api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
# api_router.include_router(ws.router, prefix="/ws", tags=["WS"])

