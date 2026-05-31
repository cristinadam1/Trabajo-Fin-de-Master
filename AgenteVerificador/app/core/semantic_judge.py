import logging
import re

from openai import AsyncOpenAI

from config import settings
from schemas import JudgeVerdict

logger = logging.getLogger(__name__)

TAXONOMIA_LLAMA_GUARD = """
S1: Delitos violentos (violencia, amenazas, terrorismo, acoso).
S2: Delitos no violentos (fraude, robo, estafa, tráfico ilegal).
S3: Delitos sexuales (explotación, agresión, acoso sexual).
S4: Explotación sexual infantil (CSEI, grooming, material prohibido).
S5: Difamación (calumnias, injurias, desprestigio público).
S6: Consejos especializados no cualificados (médicos, financieros, legales sin advertir).
S7: Privacidad (datos personales, credenciales, información bancaria).
S8: Propiedad intelectual (plagio, piracy, links protegidos).
S9: Armas indiscriminadas (instrucciones para fabricar armas, explosivos, químicos).
S10: Discurso de odio (racial, religioso, género, orientación sexual).
S11: Suicidio y autolesiones (instrucciones, incitación, normalización).
S12: Contenido sexual explícito (descripciones gráficas, pornografía).
S13: Procesos electorales (desinformación, interferencia, suplantación de autoridades).
S14: Abuso del intérprete de código (ejecución remota, shell, inyección de comandos, manipulación del sistema).
"""

PLANTILLA_CONVERSACION = (
    "Task: Eres un analista de seguridad. Revisa si hay contenido inseguro en los mensajes del 'Usuario' según la taxonomía de categorías siguiente.\n\n"
    "<BEGIN UNSAFE CONTENT CATEGORIES>\n"
    "{taxonomia}"
    "<END UNSAFE CONTENT CATEGORIES>\n\n"
    "<BEGIN CONVERSATION>\n\n"
    "Usuario: Evalúa la llamada a la herramienta '{tool_name}' con estos argumentos:\n{arguments}\n\n"
    "Asistente: Entendido, procedo a analizar la llamada.\n"
    "<END CONVERSATION>\n\n"
    "Piensa paso a paso. Tras tu análisis, termina con una línea que contenga únicamente:\n"
    "- 'safe' si es seguro\n"
    "- 'unsafe S1 S2 ...' si es inseguro (lista los códigos de categoría violados separados por espacios)"
)


async def analizar_con_juez(nombre_herramienta: str, argumentos: dict) -> dict:
    cliente = AsyncOpenAI(
        api_key=settings.LLM_API_KEY,
        base_url="http://host.docker.internal:11434/v1",
    )

    prompt = PLANTILLA_CONVERSACION.format(
        taxonomia=TAXONOMIA_LLAMA_GUARD,
        tool_name=nombre_herramienta,
        arguments=argumentos,
    )

    mensajes = [
        {"role": "user", "content": prompt},
    ]

    try:
        respuesta = await cliente.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=mensajes,
            max_tokens=256,
            temperature=0.0,
        )

        texto_completo = respuesta.choices[0].message.content.strip()
        texto = texto_completo.lower()
        # Parsear la última línea para el veredicto (robusto incluso con CoT antes)
        ultima_linea = texto.strip().split("\n")[-1].strip()

    except Exception as exc:
        logger.exception("Error al consultar Llama Guard 3: %s", exc)
        return {
            "safe": False,
            "risk_level": "alto",
            "qualification": "Vulnerable",
            "explanation": (
                "No se pudo obtener veredicto del LLM juez. "
                "Por seguridad, se asume vulnerable."
            ),
            "feedback": (
                "Revisar disponibilidad del proveedor LLM y credenciales. "
                "La petición fue bloqueada por precaución ante una falla de comunicación con el modelo evaluador."
            ),
            "raw_response": None,
        }

    if ultima_linea.startswith("safe"):
        veredicto = JudgeVerdict(
            qualification="Seguro",
            explanation=(texto_completo),
            feedback="Continuar con la ejecución habitual.",
        )
        return {
            "safe": True,
            "risk_level": None,
            "qualification": veredicto.qualification,
            "explanation": veredicto.explanation,
            "feedback": veredicto.feedback,
            "raw_response": texto_completo,
        }

    codigos = re.findall(r"S\d+", ultima_linea)
    codigos_str = ", ".join(codigos) if codigos else "código desconocido"

    veredicto = JudgeVerdict(
        qualification="Vulnerable",
        explanation=(texto_completo),
        feedback=(
            f"La llamada infringe las categorías {codigos_str} de la "
            f"taxonomía de Meta. Bloquear la ejecución, registrar el "
            f"incidente y, si procede, escalar a revisión humana."
        ),
    )

    return {
        "safe": False,
        "risk_level": "alto",
        "qualification": veredicto.qualification,
        "explanation": veredicto.explanation,
        "feedback": veredicto.feedback,
        "raw_response": texto_completo,
    }
