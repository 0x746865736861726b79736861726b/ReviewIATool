import pytest
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.testclient import TestClient
from starlette.applications import Starlette
from unittest.mock import patch

from app.middleware.logging import LoggingMiddleware


@pytest.fixture
def test_app():
    """
    Creates a Starlette test application with the LoggingMiddleware.
    """
    app = Starlette()

    @app.route("/")
    async def homepage(request: Request):
        return JSONResponse({"message": "Hello, world!"})

    app.add_middleware(LoggingMiddleware)
    return app


@pytest.mark.asyncio
async def test_logging_middleware_logs_request_and_response(test_app):
    """
    Test the LoggingMiddleware logs request and response information.
    """
    with patch("app.middleware.logging.logger.info") as mock_logger:
        client = TestClient(test_app)

        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello, world!"}

        assert mock_logger.call_count > 0
        mock_logger.assert_any_call("Request: GET http://testserver/")
        mock_logger.assert_any_call("Response: status_code=200, process_time=")


@pytest.mark.asyncio
async def test_logging_middleware_process_time_logging(test_app):
    """
    Test the LoggingMiddleware logs process time.
    """
    with patch("app.middleware.logging.logger.info") as mock_logger:
        client = TestClient(test_app)

        client.get("/")

        process_time_logged = any(
            "process_time=" in call.args[0] for call in mock_logger.call_args_list
        )
        assert process_time_logged, "Process time was not logged"
