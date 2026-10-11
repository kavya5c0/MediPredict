from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    OPENAI_API_KEY: str = "sk-placeholder"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://localhost:5432/healthcare_db"
    
    # Model Configuration
    DISEASE_MODEL_PATH: str = "models/disease_prediction.pth"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # RAG Configuration
    KNOWLEDGE_BASE_PATH: str = "data/sample_medical_knowledge.txt"
    CHROMA_PERSIST_DIR: str = "data/chroma_db"
    
    # OCR Configuration
    TESSERACT_PATH: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Load from environment if available
settings = Settings()
# Override OPENAI_API_KEY from environment variable if set
if os.getenv("OPENAI_API_KEY"):
    settings.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
