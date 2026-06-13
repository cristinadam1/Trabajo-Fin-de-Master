from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENV: str = "development"
    PROJECT_NAME: str = "Agente Verificador de Seguridad"
    DATABASE_URL: str
    LLM_API_KEY: str
    LLM_MODEL_NAME: str = "llama-guard3:1b"
    LLM_BASE_URL: str = "http://host.docker.internal:11434/v1"
    # read es la única herramienta nativa con fast-path: es solo lectura,
    # no modifica estado. write, edit y exec pasan por el pipeline completo.
    # Asumimos que el workspace no contiene symlinks maliciosos (no ha habido brecha previa)
    ALLOWED_TOOLS: str = "read"
    ALLOWED_COMMANDS: str = "git status, npm test"
    ALLOWED_COMMAND_PREFIXES: str = "ls, cat, head"
    WORKSPACE_DIR: str = "/app/sandbox"


settings = Settings()
