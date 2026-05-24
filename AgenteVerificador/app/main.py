from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import settings
from core.pipeline import evaluate_tool_call, evaluar_salida_chat
from database import Base, engine, get_db
from models import RegistroAuditoriaChat, SecurityAuditLog
from schemas import EntradaSalidaChat, ToolCallInput


class ReviewRequest(BaseModel):
    decision: Literal["aprobado", "bloqueado"]


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


@app.post("/v1/review/{log_id}")
async def review(log_id: int, body: ReviewRequest, db: Session = Depends(get_db)):
    log = db.query(SecurityAuditLog).filter(SecurityAuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")

    log.status = body.decision
    db.commit()

    return {
        "message": "Auditoría manual completada",
        "log_id": log_id,
        "status": log.status,
    }


@app.post("/v1/verificar-respuesta")
async def verificar_respuesta(
    datos: EntradaSalidaChat, db: Session = Depends(get_db)
):
    resultado = await evaluar_salida_chat(datos)

    log = RegistroAuditoriaChat(
        consulta=datos.consulta,
        respuesta=datos.respuesta,
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
        "reasons": resultado.get("reasons", []),
    }
