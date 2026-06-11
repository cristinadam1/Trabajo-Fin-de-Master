from pathlib import PurePath
from config import settings

ALLOWED_TOOLS = frozenset(
    tool.strip() for tool in settings.ALLOWED_TOOLS.split(",") if tool.strip()
)

RUTAS_SENSIBLES = frozenset({
    "/etc/passwd", "/etc/shadow", "/etc/",
    "/var/log", "/var/",
    "/root/", "/sys/", "/proc/", "/boot/",
    "/usr/bin/", "/usr/lib/",
    ".ssh", "id_rsa", "id_ed25519",
    "authorized_keys", "known_hosts", ".pgpass",
    ".aws/credentials", ".azure/", ".gcloud/",
    "../", "..\\",
    ".bash_history", ".zsh_history",
    "~/.bash_history", "~/.zsh_history",
})


def _detectar_ruta_sensible(argumentos: dict) -> bool:
    def _recurse(obj):
        if isinstance(obj, dict):
            return any(_recurse(v) for v in obj.values())
        if isinstance(obj, list):
            return any(_recurse(item) for item in obj)
        if isinstance(obj, str):
            lower = obj.lower()
            for patron in RUTAS_SENSIBLES:
                if patron in lower:
                    return True
            try:
                partes = PurePath(obj).parts
                if ".." in partes:
                    return True
            except TypeError:
                pass
        return False
    return _recurse(argumentos)


def check_allowlist(tool_name: str, arguments: dict | None = None) -> dict:
    if tool_name not in ALLOWED_TOOLS:                                              # No está en la lista
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}    # Continúa a las otras capas
    if arguments and _detectar_ruta_sensible(arguments):                            # Detecta ruta sensible
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}    # Continúa a las otras capas
    return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}        # Está permitido y no se detectan riesgos, se salta el resto de capas para optimizar rendimiento
