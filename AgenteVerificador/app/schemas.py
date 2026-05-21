from datetime import datetime

from pydantic import BaseModel


class ToolCallInput(BaseModel):
    tool_name: str
    arguments: dict
    context_user_id: str | None = None
    timestamp: datetime | None = None
