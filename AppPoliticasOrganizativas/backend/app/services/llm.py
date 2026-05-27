import os
import json
import httpx
from fastapi import HTTPException, status

from services.cliente_portatil import AgenteVerificadorClient


LLM_API_URL = os.getenv("LLM_API_URL", "http://host.docker.internal:11434/api/generate")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2-abliterated")
VERIFICADOR_URL = os.getenv("VERIFICADOR_URL", "http://localhost:8000")

verificador = AgenteVerificadorClient(VERIFICADOR_URL)


def generate_policy_content(input_text: str) -> dict:
    prompt = f"""Genera políticas organizativas para: {input_text}

POLITICAS: desarrolla aquí el contenido principal de tu respuesta (3 puntos)
1.
2.
3.

BUENAS PRACTICAS: aquí los aspectos complementarios o consejos (2 puntos)
1.
2.

ACCIONES PROHIBIDAS: aquí lo que NO se debe hacer o lo que hay que evitar (2 puntos)
1.
2.

RIESGOS: aquí los posibles riesgos o advertencias (2 puntos)
1.
2.

EXPLICACION: aquí un resumen o explicación final
-"""

    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(LLM_API_URL, json=payload, headers=headers)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"LLM API error: {response.status_code}"
                )
            data = response.json()
            content = data.get("response", "")

# Verificar la respuesta con el agente de seguridad (cliente portátil)
            try:
                resultado = verificador.verificar_respuesta(input_text, content)

                if resultado["status"] == "aprobado":
                    pass  # Seguro, continuar

                elif resultado["status"] == "pendiente_revision":
                    # Esperar a que un humano revise (máx 5 minutos)
                    resultado_final = verificador.esperar_revision(
                        resultado["log_id"], tipo="chat", timeout=300
                    )
                    if resultado_final["status"] != "aprobado":
                        raise HTTPException(
                            status_code=403,
                            detail=f"Respuesta bloqueada tras revisión humana: {resultado_final.get('reasons', '')}"
                        )

                else:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Respuesta bloqueada por el agente de seguridad: {resultado.get('reasons', [])}"
                    )

            except httpx.ConnectError:
                pass  # Si el agente no está disponible, continuar sin verificar

            return parse_llm_response(content)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se puede conectar al servicio LLM. Verifica la configuración de LLM_API_URL."
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM service timeout"
        )


def parse_llm_response(content: str) -> dict:
    try:
        content = content.strip()
        
        result = {
            "politicas": "",
            "buenas_practicas": "",
            "acciones_prohibidas": "",
            "riesgos": "",
            "explicacion": ""
        }
        
        lines = content.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            line_clean = line.replace("*", "").replace("-", "").strip()
            
            if not line_clean:
                continue
                
            upper = line_clean.upper()
            if "POLITICA" in upper:
                current_section = "politicas"
            elif "BUENA" in upper and "PRACTICA" in upper:
                current_section = "buenas_practicas"
            elif "PROHIBID" in upper:
                current_section = "acciones_prohibidas"
            elif "RIESGO" in upper:
                current_section = "riesgos"
            elif "EXPLIC" in upper:
                current_section = "explicacion"
            elif current_section and line_clean:
                if len(line_clean) > 5:
                    if result[current_section]:
                        result[current_section] += " | " + line_clean
                    else:
                        result[current_section] = line_clean
        
        for key in result:
            if not result[key]:
                result[key] = content[:400] if key == "politicas" else "No disponible"
        
        return result
    except Exception:
        return {
            "politicas": content[:500],
            "buenas_practicas": "No disponible",
            "acciones_prohibidas": "No disponible",
            "riesgos": "No disponible",
            "explicacion": "No disponible"
        }