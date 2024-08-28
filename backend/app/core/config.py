from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    DEBUG: bool
    MODEL_NAME: str
    EMBEDDING_MODEL_NAME : str = "paraphrase-MiniLM-L6-v2"
    MAX_LENGTH: int
    CONTEXT_LENGTH: int = 2000 
    HOST: str
    PORT: int
    VECTOR_DIMENSION: int
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    DATABASE_URL: str
    TEST_DATABASE_URL : str
    FAISS_OPTIMIZATION_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = "./core/.env"

settings = Settings()