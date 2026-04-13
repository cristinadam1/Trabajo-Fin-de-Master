import os
import json
import httpx
from fastapi import HTTPException, status


LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/generar")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")


def generate_policy_content(input_text: str) -> dict:
    prompt = f"""Genera políticas organizativas para: {input_text}

Responde en español, texto plano. Formato exacto:

POLITICAS:
1. 
2. 
3. 

BUENAS PRACTICAS:
1. 
2. 

ACCIONES PROHIBIDAS:
1. 
2. 

RIESGOS:
1. 
2. 

EXPLICACION:
"""

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