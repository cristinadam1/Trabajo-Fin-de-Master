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


def _generar_justificacion(
    riesgo_final: str,
    razones: list[str],
    resultado_juez: dict[str, Any] | None,
) -> str:
    partes: list[str] = ["Detecciones por capa:"]
    for r in razones:
        partes.append(f"  • {r}")
    if resultado_juez:
        v = resultado_juez
        juez_texto = "Seguro" if v.get("safe") else "Inseguro"
        partes.append(
            f"  • Juez semántico: {juez_texto} "
            f"(cualificación: {v.get('qualification', 'N/A')})"
        )
        if v.get("explanation"):
            partes.append(f"   Explicación del juez: {v['explanation']}")
    riesgo_nombre = {"bajo": "Bajo", "medio": "Medio", "alto": "Alto", "critico": "Crítico"}
    partes.append(f"  • Riesgo final: {riesgo_nombre.get(riesgo_final, riesgo_final)}")
    if riesgo_final in ("alto", "critico"):
        partes.append("   Requiere revisión humana antes de continuar.")
    elif riesgo_final == "medio":
        partes.append("   Se recomienda revisión humana.")
    else:
        partes.append("   Sin riesgos detectados. Ejecución automática.")
    return "\n".join(partes)


async def evaluate_tool_call(datos: ToolCallInput) -> dict[str, Any]:
    razones: list[str] = []
    riesgo_acumulado: str | None = None

    resultado_juez: dict[str, Any] | None = None

    # Capa 1 = Allowlist (rápida, cortocircuito si es conocida y no apunta a rutas sensibles)
    resultado_allowlist = check_allowlist(datos.tool_name, datos.arguments)
    if resultado_allowlist["skip_next_layers"]:
        return {
            "risk_level": "bajo",
            "status": "aprobado",
            "tool_name": datos.tool_name,
            "reasons": ["Herramienta en lista blanca de seguridad."],
            "qualification": "",
            "explanation": None,
            "feedback": None,
        }

    # Capa 2 = Pattern Matching (rápida, regex sobre argumentos)
    resultado_patrones = escanear_argumentos(datos.arguments)
    if not resultado_patrones["safe"]:
        riesgo_patron = resultado_patrones.get("risk_level", "alto")
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, riesgo_patron)
        razones.append(
            f"[{resultado_patrones['categoria']}] "
            f"{resultado_patrones['descripcion']} "
            f"(riesgo: {riesgo_patron}, coincidencia: '{resultado_patrones['match']}')"
        )

    # Capa 3 = Sandbox Guard (rutas, path traversal)
    resultado_sandbox = inspect_arguments(datos.arguments)
    if not resultado_sandbox["safe"]:
        razones.append(resultado_sandbox["reason"])
        return {
            "risk_level": "critico",
            "status": "bloqueado",
            "tool_name": datos.tool_name,
            "reasons": razones,
            "qualification": "",
            "explanation": _generar_justificacion("critico", razones, None),
            "feedback": None,
        }

    # Capa 4 = Semantic Judge (lenta, LLM, solo si las rápidas no han rechzado)
    resultado_juez = await analizar_con_juez(
        datos.tool_name, datos.arguments,
        user_request=datos.user_request,
    )
    if not resultado_juez["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, resultado_juez["risk_level"])


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
        "qualification": resultado_juez.get("qualification", "") if resultado_juez else "",
        "explanation": _generar_justificacion(riesgo_final, razones, resultado_juez),
        "feedback": resultado_juez.get("feedback") if resultado_juez else None,
        "raw_response": resultado_juez.get("raw_response") if resultado_juez else None,
    }


async def evaluar_salida_chat(datos: EntradaSalidaChat) -> dict[str, Any]:
    razones: list[str] = []
    riesgo_acumulado: str | None = None

    # Capa 3 = Pattern Matching sobre la respuesta generada
    resultado_patrones = escanear_texto(datos.respuesta)
    if not resultado_patrones["safe"]:
        riesgo_patron = resultado_patrones.get("risk_level", "alto")
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, riesgo_patron)
        razones.append(
            f"[{resultado_patrones['categoria']}] "
            f"{resultado_patrones['descripcion']} "
            f"(riesgo: {riesgo_patron}, coincidencia: '{resultado_patrones['match']}')"
        )

    # Capa 4 = Semantic Judge sobre la respuesta generada (modo texto: solo S1-S13)
    resultado_juez = await analizar_con_juez(
        "salida_chat", {"consulta": datos.consulta, "respuesta": datos.respuesta},
        modo="texto",
        user_request=datos.consulta,
    )
    if not resultado_juez["safe"]:
        riesgo_acumulado = _maximo_riesgo(riesgo_acumulado, resultado_juez["risk_level"])
        categorias_desc = resultado_juez.get("categorias_desc", [])
        if categorias_desc:
            codigos = [c.split(":")[0] for c in categorias_desc]
            razones.append(
                f"[LlamaGuard3] Contenido inseguro detectado: "
                f"{', '.join(codigos)}"
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
        "qualification": resultado_juez.get("qualification", ""),
        "explanation": _generar_justificacion(riesgo_final, razones, resultado_juez),
        "feedback": resultado_juez.get("feedback"),
        "raw_response": resultado_juez.get("raw_response"),
        "reasons": razones,
        "categorias_desc": resultado_juez.get("categorias_desc", []),
    }
