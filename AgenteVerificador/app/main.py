from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from config import settings
from core.pipeline import evaluate_tool_call
from database import Base, engine, get_db
from models import SecurityAuditLog
from schemas import ToolCallInput


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


@app.post("/v1/verify")
async def verify(datos: ToolCallInput, db: Session = Depends(get_db)):
    resultado = await evaluate_tool_call(datos)

    log = SecurityAuditLog(
        tool_name=datos.tool_name,
        arguments=datos.arguments,
        risk_level=resultado["risk_level"],
        verdict_qualification=resultado.get("qualification", ""),
        explanation=resultado.get("explanation"),
        feedback=resultado.get("feedback"),
        status=resultado["status"],
    )
    db.add(log)
    db.commit()

    return {
        "risk_level": resultado["risk_level"],
        "status": resultado["status"],
        "tool_name": resultado["tool_name"],
        "reasons": resultado.get("reasons", []),
    }
