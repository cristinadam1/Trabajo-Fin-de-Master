import base64
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FirmaAtaque:
    categoria_owasp: str
    descripcion: str
    patron: re.Pattern


FIRMAS = [

    # LLM01 — Inyección de Prompt
    FirmaAtaque(
        categoria_owasp="LLM01",
        descripcion="Inyeccion de prompt con saltos de contexto",
        patron=re.compile(
            r"(?i)(?:ignorar|omite|olvida|desoye|sobrescribe)\s+(?:las\s+)?(?:instrucciones?|indicaciones?|prompt|contexto)"
            r"|(?:nuevas?\s+)?instrucciones?\s*(?::|son)\s*:"
            r"|system\s*(?::|prompt)\s*:.{0,50}(?:di|actua|comportate)"
            r"|simula\s+ser|finge\s+ser|pretende\s+ser"
            r"|DAN\b|do.anything.now|jailbreak"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM01",
        descripcion="Inyeccion indirecta via datos externos",
        patron=re.compile(
            r"(?i)(?:fuente|source|url|link|documento)\s*(?:\w+\s*){0,3}(?:contiene|dice|indica)"
        ),
    ),

    # LLM07 — Diseño Inseguro de Plugins (tool calls maliciosas)
    FirmaAtaque(
        categoria_owasp="LLM07",
        descripcion="Ejecucion dinamica de codigo Python",
        patron=re.compile(r"\b(?:eval|exec|compile|__import__)\s*\("),
    ),
    FirmaAtaque(
        categoria_owasp="LLM07",
        descripcion="Llamadas al sistema operativo",
        patron=re.compile(
            r"(?i)\b(?:os\.system|subprocess\.[a-z]+|os\.popen|pty\.spawn|commands\.getoutput)\s*\("
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM07",
        descripcion="Comandos shell encadenados",
        patron=re.compile(
            r"(?i)(?:;\s*(?:rm|shutdown|reboot|chmod|chown|mkfs|dd|wget|curl|bash|nc|ncat|mkfile))"
            r"|(?:\|\s*(?:bash|sh|cmd|powershell))"
            r"|(?:&&\s*(?:curl|wget|nc|ncat))"
            r"|`[^`]*?(?:bash|sh|curl|wget)`"
            r"|\$\((?:cat|curl|wget|bash)"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM07",
        descripcion="Acceso a variables de entorno o archivos de configuracion",
        patron=re.compile(
            r"(?i)(?:os\.environ|os\.getenv|os\.putenv)"
            r"|open\s*\(\s*['\"](?:/etc/|\.env|config\.)"
        ),
    ),

    # LLM08 — Agencia Excesiva
    FirmaAtaque(
        categoria_owasp="LLM08",
        descripcion="Suplantacion de identidad o peticiones en nombre de otro",
        patron=re.compile(
            r"(?i)(?:en\s+nombre\s+de|por\s+cuenta\s+de|suplantando|impersonat(?:e|ing))\s+\w+"
            r"|Authorization:\s*Bearer\s+\S+"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM08",
        descripcion="Escalada de privilegios implicita",
        patron=re.compile(
            r"(?i)(?:admin|root|superuser|sudo|chmod\s+777|modo\s+superusuario)"
        ),
    ),

    # LLM06 — Divulgación de Información Sensible
    FirmaAtaque(
        categoria_owasp="LLM06",
        descripcion="Filtracion de claves o tokens",
        patron=re.compile(
            r"(?i)(?:sk-[A-Za-z0-9]{20,}|api[_-]?key|secret|token|password|passwd)"
            r"(?:\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"])?"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06",
        descripcion="Carga util ofuscada en Base64",
        patron=re.compile(r"[A-Za-z0-9+/]{60,}={0,2}"),
    ),

    # LLM02 — Inyección SQL (Tratamiento Inseguro de Salidas)
    FirmaAtaque(
        categoria_owasp="LLM02",
        descripcion="Inyeccion SQL clasica",
        patron=re.compile(
            r"(?i)('|\")\s*(?:OR|AND)\s*['\"]?\s*['\"]?\s*=\s*['\"]"
            r"|UNION\s+(?:ALL\s+)?SELECT"
            r"|SELECT\s+\*\s+FROM"
            r"|DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET"
            r"|--\s*$|;\s*DROP|' OR '1'='1"
        ),
    ),
]

CARGA_BASE64_ALERTA = re.compile(r"[A-Za-z0-9+/]{30,}={0,2}")


def _decodificar_base64_seguro(cadena: str) -> bool:
    try:
        return len(base64.b64decode(cadena, validate=True)) > 10
    except (base64.binascii.Error, ValueError):
        return False


def _recorrer_y_escanear(valor, memo_owasp: set):
    if isinstance(valor, dict):
        for v in valor.values():
            resultado = _recorrer_y_escanear(v, memo_owasp)
            if isinstance(resultado, dict) and not resultado.get("safe", True):
                return resultado
    elif isinstance(valor, list):
        for item in valor:
            resultado = _recorrer_y_escanear(item, memo_owasp)
            if isinstance(resultado, dict) and not resultado.get("safe", True):
                return resultado
    elif isinstance(valor, str):
        for firma in FIRMAS:
            m = firma.patron.search(valor)
            if m:
                memo_owasp.add(firma.categoria_owasp)
                return {
                    "safe": False,
                    "risk_level": "alto",
                    "categoria_owasp": firma.categoria_owasp,
                    "descripcion": firma.descripcion,
                    "match": m.group(),
                }
        if CARGA_BASE64_ALERTA.search(valor) and _decodificar_base64_seguro(valor):
            memo_owasp.add("LLM06")
            return {
                "safe": False,
                "risk_level": "alto",
                "categoria_owasp": "LLM06",
                "descripcion": "Carga util ofuscada en Base64",
                "match": valor[:60],
            }
    return None


def escanear_argumentos(argumentos: dict) -> dict:
    memo_owasp: set = set()
    resultado = _recorrer_y_escanear(argumentos, memo_owasp)
    if resultado:
        return resultado
    return {"safe": True, "risk_level": None, "categorias_owasp": list(memo_owasp)}
