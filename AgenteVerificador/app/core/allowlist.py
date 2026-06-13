from pathlib import PurePath
from config import settings

ALLOWED_TOOLS = frozenset(
    tool.strip() for tool in settings.ALLOWED_TOOLS.split(",") if tool.strip()
)

ALLOWED_COMMANDS = frozenset(
    cmd.strip() for cmd in settings.ALLOWED_COMMANDS.split(",") if cmd.strip()
)

ALLOWED_COMMAND_PREFIXES = frozenset(
    p.strip() for p in settings.ALLOWED_COMMAND_PREFIXES.split(",") if p.strip()
)

RUTAS_SENSIBLES = frozenset({
    "../", "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/sudoers",
    ".ssh/", "~/.ssh/id_rsa", "~/.ssh/id_ed25519",
    ".git/config", "~/.bashrc", ".test-env", ".env",
    "/var/log/system.log", "/proc/1/cgroup", "/.dockerenv",
})

OPERADORES_SHELL = frozenset({"&&", "||", ";", "|", "`", "$(", ">", "<", "\n"})


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


def _tiene_operadores_shell(comando: str) -> bool:
    for op in OPERADORES_SHELL:
        if op in comando:
            return True
    return False


def check_allowlist(tool_name: str, arguments: dict | None = None) -> dict:
    # 1. Rutas sensibles
    # si cualquier argumento contiene rutas como /etc/passwd, ../, .ssh/, deniega el paso rápido. 
    # Esto evita que cat /etc/passwd se cuele aunque cat esté permitido
    if arguments and _detectar_ruta_sensible(arguments):
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    # 2. Herramienta exec 
    # si el comando completo está en ALLOWED_COMMANDS (git status, npm test) o su primera palabra en 
    # ALLOWED_COMMAND_PREFIXES (ls, cat, head) y no tiene operadores shell (&&, |, ;), concede fast-path. 
    # Si no cumple, lo deniega y pasa a las otras capas
    if tool_name == "exec" and arguments and "command" in arguments:
        comando = arguments["command"].strip()
        if comando in ALLOWED_COMMANDS:
            return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}
        primer_palabra = comando.split()[0] if comando else ""
        if primer_palabra in ALLOWED_COMMAND_PREFIXES:
            if not _tiene_operadores_shell(comando):
                return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    # 3. Herramientas nativas (por ejemplo read, write, edit...) 
    # Solo "read" está en ALLOWED_TOOLS (es de solo lectura y no modifica estado). Si la herramienta no está en ALLOWED_TOOLS,
    # se deniega el fast-path y pasa por pattern_matching, sandbox y juez semántico
    if tool_name not in ALLOWED_TOOLS:
        return {"allowed": False, "skip_next_layers": False, "risk_level": None}

    return {"allowed": True, "skip_next_layers": True, "risk_level": "bajo"}
