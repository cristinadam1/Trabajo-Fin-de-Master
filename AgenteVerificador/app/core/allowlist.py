from config import settings

ALLOWED_TOOLS = frozenset(
    tool.strip() for tool in settings.ALLOWED_TOOLS.split(",") if tool.strip()
)


def check_allowlist(tool_name: str) -> dict:
    if tool_name in ALLOWED_TOOLS:
        return {"allowed": True, "risk_level": "bajo"}
    return {"allowed": False, "risk_level": None}
