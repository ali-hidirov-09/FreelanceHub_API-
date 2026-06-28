from fastapi import FastAPI
from app.routers import api_router, setup_exception_handlers
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Freelance Hub API",
    summary="Project for freelansers and users",
    description="""
    Bu API lar Freelanserlar va zakaz beruvchilarni bog'lash uchun yaratilgan
    
    Features:
    - Jobs
    """,
    version="1.0.1",
    lifespan=lifespan,

    # docs_url
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",

    contact={
        "name": "Ali",
        "email": "alihidirov285@gmail.com",
        "url": "https://github.com/ali-hidirov-09"
    },

    # license
    license_info={
        "name": "MIT",
        "identifier": "MIT"
    },


    # swagger tags order / groups
    openapi_tags=[
        {
            "name": "Jobs",
            "description": "Job management"
        },
        {
            "name": "Auth",
            "description": "Auth management"
        },

    ],


    deprecated=False,
    root_path="",
    openapi_version="3.1.0"
)



@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url='/docs')


setup_exception_handlers(app=app)
app.include_router(api_router, prefix="/api/v1")