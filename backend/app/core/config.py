from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    APP_NAME: str = Field("DefaultAppName", env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")
    MODEL_NAME: str = Field("DefaultModelName", env="MODEL_NAME")
    EMBEDDING_MODEL_NAME: str = Field("paraphrase-MiniLM-L6-v2", env="EMBEDDING_MODEL_NAME")
    MAX_LENGTH: int = Field(1000, env="MAX_LENGTH")
    CONTEXT_LENGTH: int = Field(2000, env="CONTEXT_LENGTH")
    HOST: str = Field("localhost", env="HOST")
    PORT: int = Field(8000, env="PORT")
    VECTOR_DIMENSION: int = Field(384, env="VECTOR_DIMENSION")
    CHUNK_SIZE: int = Field(500, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(50, env="CHUNK_OVERLAP")
    DATABASE_URL: str = Field("sqlite:///./test.db", env="DATABASE_URL")
    TEST_DATABASE_URL: str = Field("sqlite:///./test.db", env="TEST_DATABASE_URL")
    FAISS_OPTIMIZATION_INTERVAL_HOURS: int = Field(24, env="FAISS_OPTIMIZATION_INTERVAL_HOURS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



settings = Settings(_env_file=os.path.join(os.path.dirname(__file__), '.env'))

# Print settings to verify
print(settings.dict())