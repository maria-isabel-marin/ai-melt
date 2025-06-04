# backend/app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # URL de conexión a MongoDB. Ajusta según tu entorno:
    MONGO_URI: str = "mongodb://localhost:27017"
    # Nombre de la base de datos:
    DATABASE_NAME: str = "ai_melt_db"
    # Host y puerto donde corre FastAPI/Uvicorn (opcionales):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia global:
settings = Settings()
