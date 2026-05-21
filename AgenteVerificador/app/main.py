from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

from config import settings
from database import Base, engine
import models  # noqa: F401, E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": settings.ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
