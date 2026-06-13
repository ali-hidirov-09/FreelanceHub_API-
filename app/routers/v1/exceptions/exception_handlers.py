from fastapi import Request
from fastapi.responses import JSONResponse
from .exception import ObjectNotFound

async def object_not_found_handler(request: Request, exc: ObjectNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"{exc.model_name}(id={exc.obj_id}) toplimadi."}
    )
