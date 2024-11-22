from loguru import logger
from fastapi import FastAPI

from app.middleware.logging import LoggingMiddleware
from app.api.review import router as review_router

logger.add(
    "logs/app.log", rotation="1 MB", retention="7 days", level="INFO", enqueue=True
)

app = FastAPI()

app.add_middleware(LoggingMiddleware)
app.include_router(review_router)


@app.get("/")
async def root():
    return {"message": "Review IA tool"}
