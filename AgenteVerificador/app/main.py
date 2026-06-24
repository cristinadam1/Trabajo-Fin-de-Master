import re
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config import settings
from core.pipeline import evaluate_tool_call, evaluar_salida_chat
from core.semantic_judge import TAXONOMIA_DICT
from database import Base, engine, get_db
from models import RegistroAuditoriaChat, SecurityAuditLog
from schemas import EntradaSalidaChat, ToolCallInput


class ReviewRequest(BaseModel):
    decision: Literal["aprobado", "bloqueado"]
    tipo: str = "tool"  # "tool" para tool calls, "chat" para respuestas


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

RUTA_ESTATICA = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(RUTA_ESTATICA)), name="static")


@app.get("/revision", response_class=HTMLResponse)
async def pagina_revision():
    return (RUTA_ESTATICA / "revision.html").read_text(encoding="utf-8")


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
        raw_response=resultado.get("raw_response"),
        status=resultado["status"],
    )
    db.add(log)
    db.commit()

    return {
        "log_id": log.id,
        "risk_level": resultado["risk_level"],
        "status": resultado["status"],
        "tool_name": resultado["tool_name"],
        "reasons": resultado.get("reasons", []),
        "categorias_desc": resultado.get("categorias_desc", []),
    }


@app.get("/v1/verify/{log_id}")
async def estado_verificacion(log_id: int, db: Session = Depends(get_db)):
    log = db.query(SecurityAuditLog).filter(SecurityAuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    codigos = re.findall(r"[Ss]\d+", log.feedback or "")
    categorias_desc = [
        f"{c.upper()}: {TAXONOMIA_DICT.get(c.upper(), 'desconocida')}"
        for c in codigos
    ]
    return {
        "log_id": log.id,
        "tool_name": log.tool_name,
        "risk_level": log.risk_level,
        "status": log.status,
        "reasons": log.explanation,
        "categorias_desc": categorias_desc,
        "created_at": log.created_at.isoformat(),
    }


@app.get("/v1/pending")
async def listar_pendientes(db: Session = Depends(get_db)):
    tool_logs = (
        db.query(SecurityAuditLog)
        .filter(SecurityAuditLog.status == "pendiente_revision")
        .order_by(SecurityAuditLog.created_at.desc())
        .limit(50)
        .all()
    )
    chat_logs = (
        db.query(RegistroAuditoriaChat)
        .filter(RegistroAuditoriaChat.status == "pendiente_revision")
        .order_by(RegistroAuditoriaChat.created_at.desc())
        .limit(50)
        .all()
    )
    resultado = []
    for log in tool_logs:
        feedback = log.feedback or ""
        codigos = re.findall(r"[Ss]\d+", feedback)
        categorias_desc = [
            f"{c.upper()}: {TAXONOMIA_DICT.get(c.upper(), 'desconocida')}"
            for c in codigos
        ]
        resultado.append({
            "id": log.id,
            "tipo": "tool",
            "nombre": log.tool_name,
            "argumentos": log.arguments,
            "risk_level": log.risk_level,
            "reasons": log.explanation,
            "verdict_qualification": log.verdict_qualification,
            "feedback": log.feedback,
            "raw_response": log.raw_response,
            "categorias_desc": categorias_desc,
            "created_at": log.created_at.isoformat(),
        })
    for log in chat_logs:
        feedback = log.feedback or ""
        codigos = re.findall(r"[Ss]\d+", feedback)
        categorias_desc = [
            f"{c.upper()}: {TAXONOMIA_DICT.get(c.upper(), 'desconocida')}"
            for c in codigos
        ]
        resultado.append({
            "id": log.id,
            "tipo": "chat",
            "nombre": f"consulta: {log.consulta[:50]}",
            "argumentos": {"consulta": log.consulta, "respuesta": log.respuesta},
            "risk_level": log.risk_level,
            "reasons": log.explanation,
            "verdict_qualification": log.verdict_qualification,
            "feedback": log.feedback,
            "raw_response": log.raw_response,
            "categorias_desc": categorias_desc,
            "created_at": log.created_at.isoformat(),
        })
    resultado.sort(key=lambda x: x["created_at"], reverse=True)
    return resultado


@app.post("/v1/review/{log_id}")
async def review(log_id: int, body: ReviewRequest, db: Session = Depends(get_db)):
    if body.tipo == "chat":
        log = db.query(RegistroAuditoriaChat).filter(RegistroAuditoriaChat.id == log_id).first()
    else:
        log = db.query(SecurityAuditLog).filter(SecurityAuditLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")

    log.status = body.decision
    db.commit()

    return {
        "message": "Auditoría manual completada",
        "log_id": log_id,
        "tipo": body.tipo,
        "status": log.status,
    }


@app.post("/v1/verificar-respuesta")
async def verificar_respuesta(datos: EntradaSalidaChat, db: Session = Depends(get_db)):
    resultado = await evaluar_salida_chat(datos)

    log = RegistroAuditoriaChat(
        consulta=datos.consulta,
        respuesta=datos.respuesta,
        risk_level=resultado["risk_level"],
        verdict_qualification=resultado.get("qualification", ""),
        explanation=resultado.get("explanation"),
        feedback=resultado.get("feedback"),
        raw_response=resultado.get("raw_response"),
        status=resultado["status"],
    )
    db.add(log)
    db.commit()

    return {
        "log_id": log.id,
        "risk_level": resultado["risk_level"],
        "status": resultado["status"],
        "reasons": resultado.get("reasons", []),
        "categorias_desc": resultado.get("categorias_desc", []),
    }


@app.get("/v1/verificar-respuesta/{log_id}")
async def estado_respuesta(log_id: int, db: Session = Depends(get_db)):
    log = db.query(RegistroAuditoriaChat).filter(RegistroAuditoriaChat.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    codigos = re.findall(r"[Ss]\d+", log.feedback or "")
    categorias_desc = [
        f"{c.upper()}: {TAXONOMIA_DICT.get(c.upper(), 'desconocida')}"
        for c in codigos
    ]
    return {
        "log_id": log.id,
        "consulta": log.consulta,
        "risk_level": log.risk_level,
        "status": log.status,
        "reasons": log.explanation,
        "categorias_desc": categorias_desc,
        "created_at": log.created_at.isoformat(),
    }
