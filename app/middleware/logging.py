import time

from loguru import logger
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Log the request and response information.

        Logs the request method, URL, headers and the response status code,
        process time, and headers.
        """
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            f"Response: status_code={response.status_code}, process_time={process_time:.3f}s"
        )
        logger.info(f"Headers: {dict(response.headers)}")

        return response
