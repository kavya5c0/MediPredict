"""
Real RAG (Retrieval-Augmented Generation) System - Local Version
Uses OpenAI API + Medical Knowledge Base for AI-powered responses
Optimized for local development
"""

import openai
from typing import List, Dict
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.initialized = False
        
    async def initialize(self):
        """Initialize RAG system"""
        try:
            # Check if OpenAI API key is configured
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "sk-placeholder":
                self.initialized = True
                logger.info("RAG system initialized with OpenAI API")
            else:
                logger.warning("OpenAI API key not configured, using knowledge base fallback")
                self.initialized = False
        except Exception as e:
            logger.error(f"RAG system initialization failed: {e}")
            self.initialized = False
    
    async def retrieve_relevant_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """Retrieve relevant documents from knowledge base"""
        from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE
        
        query_lower = query.lower()
        retrieved_docs = []
        
        logger.info(f"Searching for: {query_lower}")
        logger.info(f"Available categories: {list(MEDICAL_KNOWLEDGE_BASE.keys())}")
        
        # Smart search through knowledge base
        for category, data in MEDICAL_KNOWLEDGE_BASE.items():
            if isinstance(data, dict):
                # Check if category matches query
                category_match = category in query_lower
                keyword_match = any(keyword in query_lower for keyword in 
                    ["diabetes", "heart", "blood pressure", "nutrition", "exercise", "sleep", 
                     "glucose", "cholesterol", "fever", "temperature", "hot", "chills", 
                     "back pain", "backache", "spine", "headache", "pain", "cough", 
                     "breath", "cardio", "hypertension", "weight", "diet"])
                
                logger.info(f"Category: {category}, match: {category_match or keyword_match}")
                
                if category_match or keyword_match:
                    doc_text = f"{category}: "
                    for key, value in data.items():
                        if isinstance(value, list):
                            doc_text += f"{key}: {', '.join(str(v) for v in value)}. "
                        elif isinstance(value, dict):
                            doc_text += f"{key}: {value}. "
                        else:
                            doc_text += f"{key}: {value}. "
                    
                    retrieved_docs.append({
                        "content": doc_text,
                        "metadata": {"category": category, "source": "medical_knowledge_base"},
                        "distance": 0.1
                    })
        
        # If no documents found, add general health info
        if not retrieved_docs:
            logger.warning("No documents matched, adding general health info")
            retrieved_docs.append({
                "content": "General health guidelines: Maintain balanced diet, regular exercise, adequate sleep, hydration, stress management, and regular medical check-ups.",
                "metadata": {"category": "general", "source": "medical_knowledge_base"},
                "distance": 0.5
            })
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        return retrieved_docs[:n_results]
    
    async def generate_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Generate AI response using OpenAI API"""
        logger.info(f"Attempting to generate response with OpenAI API")
        logger.info(f"API Key configured: {bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != 'sk-placeholder')}")
        
        # For now, use improved fallback (OpenAI requires credits)
        logger.info("Using improved fallback response with specific medical information")
        return await self.generate_fallback_response(query, retrieved_docs)
    
    async def generate_fallback_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Generate fallback response when AI is unavailable"""
        from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE
        
        query_lower = query.lower()
        response = ""
        
        # Always provide specific information based on query
        if any(word in query_lower for word in ["fever", "temperature", "hot", "chills"]):
            response = "### Fever Information\n\n"
            response += "**Common Causes:** Viral infections (flu, cold), bacterial infections, inflammation, heat exhaustion, medications, vaccinations.\n\n"
            response += "**When to See a Doctor:**\n"
            response += "- Temperature above 103°F (39.4°C)\n"
            response += "- Fever lasting more than 3 days\n"
            response += "- Severe headache, stiff neck, confusion\n"
            response += "- Difficulty breathing or chest pain\n"
            response += "- Severe abdominal pain or vomiting\n\n"
            response += "**Home Care:** Rest, stay hydrated, take acetaminophen or ibuprofen, dress lightly."
            
        elif any(word in query_lower for word in ["back pain", "backache", "spine", "lower back"]):
            response = "### Back Pain Information\n\n"
            response += "**Common Causes:** Muscle strain, poor posture, herniated disc, arthritis, osteoporosis, sciatica.\n\n"
            response += "**Prevention:**\n"
            response += "- Maintain good posture\n"
            response += "- Exercise regularly (core strengthening)\n"
            response += "- Lift objects properly (bend knees, not waist)\n"
            response += "- Maintain healthy weight\n"
            response += "- Avoid prolonged sitting\n\n"
            response += "**When to See a Doctor:**\n"
            response += "- Pain radiating down legs\n"
            response += "- Numbness or weakness in legs\n"
            response += "- Pain after fall or injury\n"
            response += "- Difficulty controlling bladder or bowels"
            
        elif "diabetes" in query_lower:
            data = MEDICAL_KNOWLEDGE_BASE.get("diabetes", {})
            response = f"### Diabetes Information\n\n"
            response += f"**Symptoms:** {', '.join(data.get('symptoms', [])[:5])}\n\n"
            response += f"**Risk Factors:** {', '.join(data.get('risk_factors', [])[:5])}\n\n"
            response += f"**Prevention:** {', '.join(data.get('prevention', [])[:3])}"
            
        elif "blood pressure" in query_lower or "hypertension" in query_lower:
            data = MEDICAL_KNOWLEDGE_BASE.get("hypertension", {})
            response = f"### Hypertension Information\n\n"
            response += f"**Symptoms:** {', '.join(data.get('symptoms', [])[:5])}\n\n"
            response += f"**Target BP:** {', '.join(data.get('target_blood_pressure', [])[:3])}\n\n"
            response += f"**Prevention:** {', '.join(data.get('prevention', [])[:3])}"
            
        elif "heart" in query_lower or "cardio" in query_lower:
            data = MEDICAL_KNOWLEDGE_BASE.get("heart_disease", {})
            response = f"### Heart Disease Information\n\n"
            response += f"**Symptoms:** {', '.join(data.get('symptoms', [])[:5])}\n\n"
            response += f"**Risk Factors:** {', '.join(data.get('risk_factors', [])[:5])}\n\n"
            response += f"**Prevention:** {', '.join(data.get('prevention', [])[:3])}"
            
        else:
            response = "I found general health information. For specific medical concerns, please provide more details about your symptoms or condition. Maintain a balanced diet, exercise regularly, get adequate sleep, and consult healthcare professionals for specific medical advice."
        
        response += "\n\n---\n\n**Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
        
        return response
    
    async def query(self, question: str) -> Dict:
        """Complete RAG pipeline: retrieve + generate"""
        if not self.initialized:
            await self.initialize()
        
        # Retrieve relevant documents
        retrieved_docs = await self.retrieve_relevant_documents(question)
        
        # Use improved fallback response directly
        response = await self.generate_fallback_response(question, retrieved_docs)
        
        return {
            "answer": response,
            "sources": [doc["metadata"] for doc in retrieved_docs],
            "retrieved_docs_count": len(retrieved_docs),
            "using_ai": False,
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }

# Global RAG instance
rag_system = RAGSystem()
