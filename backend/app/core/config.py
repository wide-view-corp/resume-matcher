from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    MODEL_NAME: str
    MAX_LENGTH: int
    CONTEXT_LENGTH: int = 2000 
    HOST: str
    PORT: int
    VECTOR_DIMENSION: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    DATABASE_URL: str
    FAISS_OPTIMIZATION_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"

settings = Settings()