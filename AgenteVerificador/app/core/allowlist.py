ALLOWED_TOOLS = frozenset(
    {
        "read_current_time",
        "get_weather_info",
        "view_documentation",
    }
)


def check_allowlist(tool_name: str) -> dict:
    if tool_name in ALLOWED_TOOLS:
        return {"allowed": True, "risk_level": "bajo"}
    return {"allowed": False, "risk_level": None}
