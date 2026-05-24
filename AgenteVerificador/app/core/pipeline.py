import logging
from typing import Any

from core.allowlist import check_allowlist
from core.pattern_matching import escanear_argumentos, escanear_texto
from core.sandbox_guard import inspect_arguments
from core.semantic_judge import analizar_con_juez
from schemas import EntradaSalidaChat, ToolCallInput

logger = logging.getLogger(__name__)

JERARQUIA_RIESGO = {"bajo": 1, "medio": 2, "alto": 3, "critico": 4}


def _maximo_riesgo(*riesgos: str | None) -> str | None:
    niveles = [r for r in riesgos if r is not None]
    if not niveles:
        return None
    niveles.sort(key=lambda r: JERARQUIA_RIESGO.get(r, 0))
    return niveles[-1]


async def evaluate_tool_call(datos: ToolCallInput) -> dict[str, Any]:
    razones: list[str] = []
    riesgo_acumulado: str | None = None

    # Capa 1 — Allowlist
    resultado_allowlist = check_allowlist(datos.tool_name)
    if resultado_allowlist["allowed"]:
        return {
            "risk_level": "bajo",
            "status": "aprobado",
            "tool_name": datos.tool_name,
            "reasons": ["Herramienta en lista blanca de seguridad."],
        }

    # Capa 2 — Semantic Judge (análisis semántico con LLM)
    resultado_juez = await analizar_con_juez(datos.tool_name, datos.arguments)
    if not resultado_juez["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, "alto")
        razones.append(
            f"LLM juez califica como {resultado_juez['qualification']}: "
            f"{resultado_juez['explanation']}"
        )

    # Capa 3 — Pattern Matching
    resultado_patrones = escanear_argumentos(datos.arguments)
    if not resultado_patrones["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, "alto")
        razones.append(
            f"[{resultado_patrones['categoria_owasp']}] "
            f"{resultado_patrones['descripcion']} "
            f"(coincidencia: '{resultado_patrones['match']}')"
        )

    # Capa 4 — Sandbox Guard
    resultado_sandbox = inspect_arguments(datos.arguments)
    if not resultado_sandbox["safe"]:
        razones.append(resultado_sandbox["reason"])
        return {
            "risk_level": "critico",
            "status": "bloqueado",
            "tool_name": datos.tool_name,
            "reasons": razones,
        }

    # Consolidación final
    riesgo_final = riesgo_acumulado or "bajo"

    if riesgo_final == "bajo":
        status = "aprobado"
    elif riesgo_final in ("medio", "alto"):
        status = "pendiente_revision"
    else:
        status = "bloqueado"

    return {
        "risk_level": riesgo_final,
        "status": status,
        "tool_name": datos.tool_name,
        "reasons": razones,
    }


async def evaluar_salida_chat(datos: EntradaSalidaChat) -> dict[str, Any]:
    razones: list[str] = []
    riesgo_acumulado: str | None = None

    # Capa 3 — Pattern Matching sobre la respuesta generada
    resultado_patrones = escanear_texto(datos.respuesta)
    if not resultado_patrones["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, "alto")
        razones.append(
            f"[{resultado_patrones['categoria_owasp']}] "
            f"{resultado_patrones['descripcion']} "
            f"(coincidencia: '{resultado_patrones['match']}')"
        )

    # Capa 4 — Semantic Judge sobre la respuesta generada
    resultado_juez = await analizar_con_juez(
        "salida_chat", {"consulta": datos.consulta, "respuesta": datos.respuesta}
    )
    if not resultado_juez["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, "alto")
        razones.append(
            f"LLM juez califica como {resultado_juez['qualification']}: "
            f"{resultado_juez['explanation']}"
        )

    riesgo_final = riesgo_acumulado or "bajo"

    if riesgo_final == "bajo":
        status = "aprobado"
    elif riesgo_final in ("medio", "alto"):
        status = "pendiente_revision"
    else:
        status = "bloqueado"

    return {
        "risk_level": riesgo_final,
        "status": status,
        "reasons": razones,
    }
