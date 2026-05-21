from datetime import datetime, timezone

from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": settings.ENV,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
