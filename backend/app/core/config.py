from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    OPENAI_API_KEY: str = "sk-placeholder"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    MONGODB_URI: str = "mongodb://localhost:27017/healthcare_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
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

settings = Settings()
