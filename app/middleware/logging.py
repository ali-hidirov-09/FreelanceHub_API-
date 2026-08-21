import uuid
import time
import sys
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger("freelancehub")
logger.setLevel(level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        start_time = time.perf_counter()

        response = await call_next(request)

        proces_time_seconds = (time.perf_counter() - start_time)
        proces_time_ms = proces_time_seconds * 1000


        logger.info(
            f"[ID: {request_id}] | "
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Latency: {proces_time_ms: .2f}s | "
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{proces_time_seconds:.4f} s"

        return response
