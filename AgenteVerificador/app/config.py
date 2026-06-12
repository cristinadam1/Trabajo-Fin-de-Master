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
    ALLOWED_TOOLS: str = "ls,cat,head,read"
    ALLOWED_COMMANDS: str = "git status,git log,npm test,pytest"
    WORKSPACE_DIR: str = "/app/sandbox"


settings = Settings()
