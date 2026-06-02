from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ENV: str = "development"
    PROJECT_NAME: str = "Agente Verificador de Seguridad"
    DATABASE_URL: str
    LLM_API_KEY: str
    LLM_BASE_URL: str = "http://host.docker.internal:11434/v1"
    LLM_MODEL_NAME: str = "llama-guard3:1b"
    ALLOWED_TOOLS: str = "read_current_time,get_weather_info,view_documentation"


settings = Settings()
