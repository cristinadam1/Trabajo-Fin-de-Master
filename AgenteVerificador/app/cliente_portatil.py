# Cualquier aplicación puede copiar/clonar este archivo 

import time
import httpx


class AgenteVerificadorClient:
    def __init__(self, url_agente: str = "http://localhost:8001", timeout: int = 10):
        self.url = url_agente.rstrip("/")
        self.timeout = timeout

    def verificar(self, nombre_herramienta: str, argumentos: dict) -> dict:
        """Envía una tool call al agente y devuelve la decisión."""
        respuesta = httpx.post(
            f"{self.url}/v1/verify",
            json={"tool_name": nombre_herramienta, "arguments": argumentos},
            timeout=self.timeout,
        )
        respuesta.raise_for_status()
        return respuesta.json()

    def verificar_respuesta(self, consulta: str, respuesta_llm: str) -> dict:
        """Verifica una respuesta de chat antes de mostrarla al usuario."""
        respuesta = httpx.post(
            f"{self.url}/v1/verificar-respuesta",
            json={"consulta": consulta, "respuesta": respuesta_llm},
            timeout=self.timeout,
        )
        respuesta.raise_for_status()
        return respuesta.json()

    def consultar_estado(self, log_id: int, tipo: str = "verify") -> dict:
        """
        Consulta el estado actual de una verificación.
        - tipo "verify": tool call
        - tipo "chat": respuesta de chat
        """
        if tipo == "chat":
            url = f"{self.url}/v1/verificar-respuesta/{log_id}"
        else:
            url = f"{self.url}/v1/verify/{log_id}"
        respuesta = httpx.get(url, timeout=self.timeout)
        respuesta.raise_for_status()
        return respuesta.json()

    def esperar_revision(
        self,
        log_id: int,
        tipo: str = "verify",
        intervalo: int = 3,
        timeout: int = 300,
    ) -> dict:
        
        # Espera hasta que un humano revise la petición pendiente.
        # Devuelve el estado final (aprobado o bloqueado).
        # Lanza TimeoutError si pasa el tiempo máximo.

        inicio = time.time()
        while True:
            estado = self.consultar_estado(log_id, tipo)

            if estado["status"] != "pendiente_revision":
                return estado

            if time.time() - inicio > timeout:
                raise TimeoutError(
                    f"Log {log_id} sigue pendiente tras {timeout}s de espera"
                )

            time.sleep(intervalo)
