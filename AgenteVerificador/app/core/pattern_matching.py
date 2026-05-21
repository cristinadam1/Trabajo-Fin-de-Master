import re
import base64

PATRONES_SOSPECHOSOS = [
    ("ejecucion_dinamica_python", re.compile(
        r"\b(?:eval|exec)\s*\(|__import__\s*\(|compile\s*\("
    )),
    ("carga_util_base64", re.compile(
        r"[A-Za-z0-9+/]{40,}=*\s*"
    )),
    ("comandos_consola_peligrosos", re.compile(
        r";\s*(?:rm|shutdown|reboot|chmod|chown|mkfs|dd|wget|curl|bash)"
        r"|\|\s*(?:bash|sh|cmd|powershell)"
        r"|&&\s*(?:curl|wget|nc|ncat)"
    )),
    ("inyeccion_sql", re.compile(
        r"('|\")\s*(?:OR|AND)\s*['\"]?\s*['\"]?\s*=\s*['\"]"
        r"|--\s*$|UNION\s+ALL\s+SELECT|SELECT\s+\*\s+FROM"
        r"|DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO"
    )),
]


def _es_base64_legible(cadena: str) -> bool:
    try:
        decodificada = base64.b64decode(cadena, validate=True)
        return len(decodificada) > 10
    except (base64.binascii.Error, ValueError):
        return False


def escanear_argumentos(argumentos: dict) -> dict:
    def _recorrer(valor):
        if isinstance(valor, dict):
            for v in valor.values():
                resultado = _recorrer(v)
                if resultado:
                    return resultado
        elif isinstance(valor, list):
            for item in valor:
                resultado = _recorrer(item)
                if resultado:
                    return resultado
        elif isinstance(valor, str):
            for nombre, patron in PATRONES_SOSPECHOSOS:
                if patron.search(valor):
                    return {
                        "safe": False,
                        "risk_level": "alto",
                        "pattern": nombre,
                        "match": patron.search(valor).group(),
                    }
            if len(valor) > 30 and _es_base64_legible(valor):
                return {
                    "safe": False,
                    "risk_level": "alto",
                    "pattern": "carga_util_base64",
                    "match": valor[:60],
                }
        return None

    resultado = _recorrer(argumentos)
    if resultado:
        return resultado
    return {"safe": True, "risk_level": None}
