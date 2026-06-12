from pathlib import Path

from config import settings

WORKSPACE_DIR = Path(settings.WORKSPACE_DIR).resolve()

SENSITIVE_PATTERNS = frozenset({
    "/etc/", "/var/", "/root/", "/sys/", "/proc/", "/boot/",
    "/usr/bin/", "/usr/lib/", "/usr/share/",
    "/windows/", "/winnt/", "\\windows\\", "\\winnt\\",
    "system32", "cmd.exe", "powershell.exe",
})


def _contains_sensitive(value: str) -> bool:
    lower = value.lower()
    return any(pattern in lower for pattern in SENSITIVE_PATTERNS)


def _is_path_safe(value: str) -> bool:
    try:
        resolved = (WORKSPACE_DIR / str(value)).resolve()
        return resolved.is_relative_to(WORKSPACE_DIR)
    except Exception:
        return False


def inspect_arguments(arguments: dict) -> dict:
    def _recurse(obj):
        if isinstance(obj, dict):
            for v in obj.values():
                result = _recurse(v)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = _recurse(item)
                if result:
                    return result
        elif isinstance(obj, str):
            if _contains_sensitive(obj):
                return {
                    "safe": False,
                    "risk_level": "critico",
                    "reason": f"Detectada referencia estática prohibida: '{obj}'",
                }
            if "/" in obj or "\\" in obj:
                if not _is_path_safe(obj):
                    return {
                        "safe": False,
                        "risk_level": "critico",
                        "reason": f"Violación de Sandbox: acceso fuera del workspace ({obj})",
                    }
        return None

    result = _recurse(arguments)
    if result:
        return result
    return {"safe": True, "risk_level": None}
