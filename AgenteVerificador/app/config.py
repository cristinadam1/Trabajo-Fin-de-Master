from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENV: str = "development"
    PROJECT_NAME: str = "Agente Verificador de Seguridad"
    DATABASE_URL: str
    LLM_API_KEY: str
    LLM_MODEL_NAME: str = "llama-guard3:1b"


settings = Settings()
