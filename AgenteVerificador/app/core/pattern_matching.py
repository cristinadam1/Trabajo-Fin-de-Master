import base64
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FirmaAtaque:
    categoria_owasp: str
    descripcion: str
    patron: re.Pattern


FIRMAS = [

    # LLM01:2025 = Prompt Injection
    FirmaAtaque(
        categoria_owasp="LLM01:2025",
        descripcion="Inyeccion de prompt con saltos de contexto",
        patron=re.compile(
            r"(?i)(?:ignorar|omite|olvida|desoye|sobrescribe)\s+(?:las\s+)?(?:instrucciones?|indicaciones?|prompt|contexto)"
            r"|(?:nuevas?\s+)?instrucciones?\s*(?::|son)\s*:"
            r"|system\s*:.*?(?:di|act[úu]a|comportate|ignora|olvida|omite|instrucciones)"
            r"|simula\s+ser|finge\s+ser|pretende\s+ser"
            r"|DAN\b|do.anything.now|jailbreak"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM01:2025",
        descripcion="Inyeccion indirecta via datos externos",
        patron=re.compile(
            r"(?i)(?:fuente|source|url|link|documento)\s*(?:\w+\s*){0,3}(?:contiene|dice|indica)"
        ),
    ),

    # LLM02:2025 = Sensitive Information Disclosure
    FirmaAtaque(
        categoria_owasp="LLM02:2025",
        descripcion="Filtracion de claves o tokens",
        patron=re.compile(
            r"(?i)(?:sk-[A-Za-z0-9]{20,}|api[_-]?key|secret|token|password|passwd)"
            r"(?:\s*[:=]\s*['\"][A-Za-z0-9_\-]{8,}['\"])?"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM02:2025",
        descripcion="Carga util ofuscada en Base64",
        patron=re.compile(r"[A-Za-z0-9+/]{60,}={0,2}"),
    ),
    FirmaAtaque(
        categoria_owasp="LLM02:2025",
        descripcion="Phishing: suplantacion de identidad corporativa",
        patron=re.compile(
            r"(?i)(?:estimado\s+(?:cliente|usuario)|apreciado\s+(?:cliente|usuario))"
            r"|(?:soporte\s+técnico|departamento\s+de\s+seguridad)\s*(?:\w+\s*){0,3}(?:solicita|notifica|informa)"
            r"|(?:haga\s+clic|click\s+aquí|verifique\s+su\s+cuenta|actualice\s+su\s+información)"
            r"|(?:https?://(?:bit\.ly|tinyurl|shorturl|rb\.gy|ow\.ly|short\.link))"
            r"|(?:suplantando|haciéndose\s+pasar|falsificando)"
            r"|(?:correo\s+urgente|respuesta\s+inmediata|su\s+cuenta\s+será\s+(?:suspendida|bloqueada|cerrada))"
        ),
    ),

    # LLM05:2025 = Improper Output Handling
    FirmaAtaque(
        categoria_owasp="LLM05:2025",
        descripcion="Inyeccion SQL clasica",
        patron=re.compile(
            r"(?i)('|\")\s*(?:OR|AND)\s*['\"]?\s*['\"]?\s*=\s*['\"]"
            r"|UNION\s+(?:ALL\s+)?SELECT"
            r"|SELECT\s+\*\s+FROM"
            r"|DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO|UPDATE\s+\w+\s+SET"
            r"|--\s*$|;\s*DROP|' OR '1'='1"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM05:2025",
        descripcion="Inyeccion SQL automatizada ciega (Time-based / Boolean)",
        patron=re.compile(
            r"(?i)(?:SLEEP|WAITFOR\s+DELAY|BENCHMARK)\s*\("
            r"|SUBSTRING\s*\(.*?,\s*\d+,\s*1\s*\)"
            r"|information_schema"
            r"|ASCII\s*\(\s*SUBSTRING"
            r"|CASE\s+WHEN.*?THEN\s+SLEEP"
            r"|IF\s*\(.*?SLEEP"
        ),
    ),

    # LLM06:2025 = Excessive Agency
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Ejecucion dinamica de codigo Python",
        patron=re.compile(r"\b(?:eval|exec|compile|__import__)\s*\("),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Llamadas al sistema operativo",
        patron=re.compile(
            r"(?i)\b(?:os\.system|subprocess\.[a-z]+|os\.popen|pty\.spawn|commands\.getoutput)\s*\("
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
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
        categoria_owasp="LLM06:2025",
        descripcion="Acceso a variables de entorno o archivos de configuracion",
        patron=re.compile(
            r"(?i)(?:os\.environ|os\.getenv|os\.putenv)"
            r"|open\s*\(\s*['\"](?:/etc/|\.env|config\.)"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Suplantacion de identidad o peticiones en nombre de otro",
        patron=re.compile(
            r"(?i)(?:en\s+nombre\s+de|por\s+cuenta\s+de|suplantando|impersonat(?:e|ing))\s+\w+"
            r"|Authorization:\s*Bearer\s+\S+"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Escalada de privilegios implicita",
        patron=re.compile(
            r"(?i)(?:admin|root|superuser|sudo|chmod\s+777|modo\s+superusuario)"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Malware nativo: keylogger con API de Windows",
        patron=re.compile(
            r"(?i)(?:GetAsyncKeyState|SetWindowsHookEx|GetForegroundWindow|GetWindowText)"
            r"|KEY_LOGGER|keylogger|KeyboardProc|WH_KEYBOARD"
            r"|(?:WriteFile|CreateFile)\s*\(.*?[Kk]ey[Hh]ook"
            r"|#include\s*<Windows\.h>"
            r"|#include\s*<winuser\.h>"
            r"|LRESULT\s+CALLBACK\s+KeyboardProc"
        ),
    ),
    FirmaAtaque(
        categoria_owasp="LLM06:2025",
        descripcion="Malware: persistencia, conexion inversa o descarga de payload",
        patron=re.compile(
            r"(?i)(?:RegSetValue|CreateService|StartService|schtasks|SC\s+CREATE)"
            r"|(?:CreateRemoteThread|VirtualAllocEx|WriteProcessMemory)"
            r"|(?:socket\s*\(\s*AF_INET|connect\s*\(\s*sock|WSAStartup)"
            r"|(?:URLDownloadToFile|WebClient|DownloadString|WinHttpOpen)"
        ),
    ),

    # LLM07:2025 = System Prompt Leakage
    FirmaAtaque(
        categoria_owasp="LLM07:2025",
        descripcion="Intento de revelar el prompt del sistema",
        patron=re.compile(
            r"(?i)(?:c[uú]al(?:es)?\s+son?\s+tu(?:s)?\s+(?:prompt|instrucci[oó]n(?:es)?|system\s+prompt|configuraci[oó]n))"
            r"|(?:dime\s+tu(?:s)?\s+(?:prompt|instrucci[oó]n(?:es)?|system\s+prompt))"
            r"|(?:mu[eé]strame\s+tu(?:s)?\s+(?:prompt|instrucci[oó]n(?:es)?|configuraci[oó]n))"
            r"|(?:repite\s+tu(?:s)?\s+(?:prompt|instrucciones|system\s+prompt))"
            r"|(?:qu[eé]\s+(?:instrucciones|prompt|reglas)\s+tienes)"
            r"|(?:reveal|show|print)\s+(?:your\s+)?(?:system\s+)?prompt"
            r"|(?:ignore\s+previous\s+instructions.*?(?:show|reveal|tell))"
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
            memo_owasp.add("LLM02:2025")
            return {
                "safe": False,
                "risk_level": "alto",
                "categoria_owasp": "LLM02:2025",
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


def escanear_texto(texto: str) -> dict:
    memo_owasp: set = set()
    resultado = _recorrer_y_escanear(texto, memo_owasp)
    if resultado:
        return resultado
    return {"safe": True, "risk_level": None, "categorias_owasp": list(memo_owasp)}
