from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from database import Base


class SecurityAuditLog(Base):
    __tablename__ = "security_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    tool_name = Column(String, nullable=False)
    arguments = Column(JSON, nullable=False)
    risk_level = Column(String, nullable=False)
    verdict_qualification = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class RegistroAuditoriaChat(Base):
    __tablename__ = "chat_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    consulta = Column(Text, nullable=False)
    respuesta = Column(Text, nullable=False)
    risk_level = Column(String, nullable=False)
    verdict_qualification = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
