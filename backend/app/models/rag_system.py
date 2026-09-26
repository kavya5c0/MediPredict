"""
Real RAG (Retrieval-Augmented Generation) System
Uses OpenAI API + ChromaDB for AI-powered medical responses
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import openai
from typing import List, Dict
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self.initialized = False
        
    async def initialize(self):
        """Initialize RAG system with vector database and embedding model"""
        try:
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.PersistentClient(
                path="data/chroma_db",
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="medical_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            
            # Check if collection is empty, populate with data
            if self.collection.count() == 0:
                await self.populate_knowledge_base()
            
            self.initialized = True
            logger.info("RAG system initialized successfully")
            
        except Exception as e:
            logger.error(f"RAG system initialization failed: {e}")
            self.initialized = False
    
    async def populate_knowledge_base(self):
        """Populate vector database with medical knowledge"""
        from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE
        
        documents = []
        metadatas = []
        ids = []
        
        # Convert medical knowledge to documents
        for category, data in MEDICAL_KNOWLEDGE_BASE.items():
            if isinstance(data, dict):
                doc_text = f"{category}: "
                for key, value in data.items():
                    if isinstance(value, list):
                        doc_text += f"{key}: {', '.join(str(v) for v in value)}. "
                    elif isinstance(value, dict):
                        doc_text += f"{key}: {value}. "
                    else:
                        doc_text += f"{key}: {value}. "
                
                documents.append(doc_text)
                metadatas.append({"category": category, "source": "medical_knowledge_base"})
                ids.append(f"{category}_knowledge")
        
        # Add documents to collection
        if documents:
            embeddings = self.embedding_model.encode(documents).tolist()
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to knowledge base")
    
    async def retrieve_relevant_documents(self, query: str, n_results: int = 3) -> List[Dict]:
        """Retrieve relevant documents using vector similarity search"""
        if not self.initialized:
            logger.warning("RAG system not initialized")
            return []
        
        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query]).tolist()
            
            # Search for similar documents
            results = self.collection.query(
                query_embeddings=query_embedding,
                n_results=n_results
            )
            
            # Format results
            retrieved_docs = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    retrieved_docs.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })
            
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return []
    
    async def generate_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Generate AI response using OpenAI API"""
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "sk-placeholder":
            logger.warning("OpenAI API key not configured, using fallback")
            return await self.generate_fallback_response(query, retrieved_docs)
        
        try:
            # Prepare context from retrieved documents
            context = "\n\n".join([doc["content"] for doc in retrieved_docs])
            
            # Prepare messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful medical assistant AI. Provide accurate, evidence-based health information based on the provided context. 
                    Always include a disclaimer that this is not medical advice and users should consult healthcare professionals.
                    Be thorough but concise, and prioritize patient safety."""
                },
                {
                    "role": "user",
                    "content": f"""Context from medical knowledge base:
{context}

User question: {query}

Please provide a helpful, evidence-based response using the context above."""
                }
            ]
            
            # Call OpenAI API using newer client
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return await self.generate_fallback_response(query, retrieved_docs)
    
    async def generate_fallback_response(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Generate fallback response when AI is unavailable"""
        from app.data.medical_knowledge import MEDICAL_KNOWLEDGE_BASE
        
        query_lower = query.lower()
        
        # Use retrieved documents to build response
        if retrieved_docs:
            context = "\n\n".join([doc["content"] for doc in retrieved_docs])
            response = f"Based on medical knowledge:\n\n{context}\n\n"
        else:
            # Fallback to knowledge base search
            response = ""
            if "diabetes" in query_lower:
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
            else:
                response = "I found general health information. Maintain a balanced diet, exercise regularly, get adequate sleep, and consult healthcare professionals for specific medical advice."
        
        response += "\n\n---\n\n**Disclaimer:** This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition."
        
        return response
    
    async def query(self, question: str) -> Dict:
        """Complete RAG pipeline: retrieve + generate"""
        if not self.initialized:
            await self.initialize()
        
        # Retrieve relevant documents
        retrieved_docs = await self.retrieve_relevant_documents(question)
        
        # Generate response
        response = await self.generate_response(question, retrieved_docs)
        
        return {
            "answer": response,
            "sources": [doc["metadata"] for doc in retrieved_docs],
            "retrieved_docs_count": len(retrieved_docs),
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }

# Global RAG instance
rag_system = RAGSystem()