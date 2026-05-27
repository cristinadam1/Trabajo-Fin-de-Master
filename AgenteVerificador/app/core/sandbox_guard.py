from pathlib import PurePath, PurePosixPath, PureWindowsPath

SENSITIVE_PATTERNS = frozenset({
    "/etc/",
    "/var/",
    "/root/",
    "/sys/",
    "/proc/",
    "/boot/",
    "/usr/bin/",
    "/usr/lib/",
    "/usr/share/",
    "/windows/",
    "/winnt/",
    "\\windows\\",
    "\\winnt\\",
    "system32",
    "cmd.exe",
    "powershell.exe",
})


def _is_path_traversal(value: str) -> bool:
    try:
        path = PurePath(value)
    except TypeError:
        return False

    parts = path.parts

    if ".." in parts:
        return True

    try:
        posix = PurePosixPath(value)
        if ".." in posix.parts:
            return True
    except TypeError:
        pass

    try:
        win = PureWindowsPath(value)
        if ".." in win.parts:
            return True
    except TypeError:
        pass

    return False


def _is_absolute_path(value: str) -> bool:
    try:
        path = PurePath(value)
        return path.is_absolute()
    except TypeError:
        return False


def _contains_sensitive(value: str) -> bool:
    lower = value.lower()
    return any(pattern in lower for pattern in SENSITIVE_PATTERNS)


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
            if _is_path_traversal(obj):
                return {
                    "safe": False,
                    "risk_level": "critico",
                    "reason": f"Detectado patrón de salto de directorio: '{obj}'",
                }
            if _is_absolute_path(obj):
                return {
                    "safe": False,
                    "risk_level": "critico",
                    "reason": f"Detectada ruta absoluta: '{obj}'",
                }
            if _contains_sensitive(obj):
                return {
                    "safe": False,
                    "risk_level": "critico",
                    "reason": f"Detectada referencia a archivo o ruta sensible: '{obj}'",
                }
        return None

    result = _recurse(arguments)
    if result:
        return result
    return {"safe": True, "risk_level": None}
