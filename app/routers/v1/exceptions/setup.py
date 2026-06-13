from fastapi import FastAPI

from .exception import ObjectNotFound
from .exception_handlers import object_not_found_handler

def setup_exception_handlers(app:FastAPI):
    app.add_exception_handler(ObjectNotFound, object_not_found_handler)
