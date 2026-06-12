from pathlib import PurePath
from config import settings

ALLOWED_TOOLS = frozenset(
    tool.strip() for tool in settings.ALLOWED_TOOLS.split(",") if tool.strip()
)

ALLOWED_COMMANDS = frozenset(
    cmd.strip() for cmd in settings.ALLOWED_COMMANDS.split(",") if cmd.strip()
)

RUTAS_SENSIBLES = frozenset({
    "../", "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/sudoers",
    ".ssh/", "~/.ssh/id_rsa", "~/.ssh/id_ed25519",
    ".git/config", "~/.bashrc", ".test-env", ".env",
    "/var/log/system.log", "/proc/1/cgroup", "/.dockerenv",
    "/home/", "/tmp/",
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
    # Las rutas sensibles se evalúan primero sobre cualquier herramienta
    if arguments and _detectar_ruta_sensible(arguments):
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    # Si la herramienta es 'exec' (shell), validar comando exacto
    if tool_name == "exec" and arguments and "command" in arguments:
        comando = arguments["command"].strip()
        if comando in ALLOWED_COMMANDS:
            return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    # Herramientas nativas permitidas (lectura, listado, etc.)
    if tool_name not in ALLOWED_TOOLS:
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}
