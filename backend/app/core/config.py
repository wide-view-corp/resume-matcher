from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    MODEL_NAME: str
    MAX_LENGTH: int
    HOST: str
    PORT: int
    VECTOR_DIMENSION: int = 384
    CHUNK_SIZE: int = 200
    CHUNK_OVERLAP: int = 0
    DATABASE_URL: str
    FAISS_OPTIMIZATION_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"

settings = Settings()