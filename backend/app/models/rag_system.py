from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from typing import List, Dict
import os
from app.core.config import settings
import re

class MedicalRAGSystem:
    def __init__(self):
        try:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL
            )
        except Exception as e:
            print(f"Failed to initialize embeddings: {e}")
            self.embeddings = None
        
        self.vectorstore = None
        self.qa_chain = None
        self.use_keyword_fallback = False
        
        # Check if OpenAI key is a placeholder or invalid
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
            print("OpenAI API key not configured, using keyword-based fallback")
            self.llm = None
            self.use_keyword_fallback = True
        else:
            try:
                self.llm = OpenAI(
                    openai_api_key=settings.OPENAI_API_KEY,
                    temperature=0.7
                )
            except Exception as e:
                print(f"Failed to initialize LLM: {e}, using keyword-based fallback")
                self.llm = None
                self.use_keyword_fallback = True
        
    def initialize_vectorstore(self, documents: List[str] = None):
        """Initialize ChromaDB vector store with medical documents"""
        if not self.embeddings:
            print("Embeddings not available, skipping vector store initialization")
            return
            
        persist_dir = settings.CHROMA_PERSIST_DIR
        
        try:
            if os.path.exists(persist_dir):
                self.vectorstore = Chroma(
                    persist_directory=persist_dir,
                    embedding_function=self.embeddings
                )
            else:
                if documents:
                    self.create_knowledge_base(documents)
                else:
                    os.makedirs(persist_dir, exist_ok=True)
                    self.vectorstore = Chroma(
                        persist_directory=persist_dir,
                        embedding_function=self.embeddings
                    )
        except Exception as e:
            print(f"Failed to initialize vector store: {e}")
    
    def create_knowledge_base(self, documents: List[str]):
        """Create knowledge base from medical documents"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        texts = []
        for doc in documents:
            chunks = text_splitter.split_text(doc)
            texts.extend(chunks)
        
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIR
        )
    
    def setup_qa_chain(self):
        """Setup RAG chain for medical queries"""
        if self.use_keyword_fallback:
            print("Using keyword-based fallback, skipping QA chain setup")
            return
            
        if not self.vectorstore:
            self.initialize_vectorstore()
        
        if not self.vectorstore or not self.llm:
            print("Cannot setup QA chain: missing vectorstore or LLM")
            return
        
        try:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            )
            
            prompt_template = """
            You are a medical AI assistant. Use the following pieces of context to answer the question about health and medical conditions.
            If you don't know the answer based on the context, say that you don't know and suggest consulting a healthcare professional.
            Always include a disclaimer that this is not medical advice.
            
            Context: {context}
            
            Question: {question}
            
            Answer:
            """
            
            PROMPT = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": PROMPT},
                return_source_documents=True
            )
        except Exception as e:
            print(f"Failed to setup QA chain: {e}")
            self.use_keyword_fallback = True
    
    def _keyword_based_response(self, question: str) -> Dict:
        """Fallback keyword-based response when OpenAI is not available"""
        question_lower = question.lower()
        
        # Define simple keyword-based responses
        responses = {
            "diabetes": "Diabetes is a condition where your body has trouble regulating blood sugar. Type 1 diabetes is usually diagnosed in childhood, while Type 2 is often related to lifestyle factors. Key management strategies include monitoring blood sugar, maintaining a healthy diet, regular exercise, and taking prescribed medications. Please consult with a healthcare professional for personalized advice.",
            
            "hypertension|blood pressure|high bp": "Hypertension (high blood pressure) is when the force of blood against artery walls is consistently too high. It can lead to heart disease and stroke. Management includes reducing sodium intake, maintaining a healthy weight, regular exercise, limiting alcohol, and taking prescribed medications. Regular monitoring is important. Please consult a healthcare professional.",
            
            "heart|cardiac|cardiovascular": "Heart health is crucial for overall wellbeing. Key factors include maintaining healthy cholesterol levels, blood pressure, regular exercise, a balanced diet, and not smoking. Warning signs of heart problems include chest pain, shortness of breath, and irregular heartbeat. If you experience these symptoms, seek immediate medical attention.",
            
            "asthma|breathing|respiratory": "Asthma is a respiratory condition causing breathing difficulties. Triggers can include allergens, exercise, cold air, or stress. Management involves avoiding triggers, using prescribed inhalers, and having an asthma action plan. If you experience severe breathing difficulties, seek emergency medical care.",
            
            "diet|nutrition|food|eating": "A balanced diet is essential for good health. Focus on fruits, vegetables, whole grains, lean proteins, and healthy fats. Limit processed foods, added sugars, and excessive salt. Stay hydrated and consider portion sizes. Nutritional needs vary by individual, so consult a healthcare professional or registered dietitian for personalized advice.",
            
            "exercise|physical activity|workout": "Regular physical activity is crucial for health. Adults should aim for at least 150 minutes of moderate aerobic activity or 75 minutes of vigorous activity per week, plus strength training twice weekly. Always consult a healthcare provider before starting a new exercise program, especially if you have existing health conditions.",
            
            "stress|mental health|anxiety|depression": "Mental health is as important as physical health. Stress management techniques include regular exercise, adequate sleep, mindfulness, and social connections. If you're experiencing persistent anxiety or depression, please seek help from a mental health professional. There's no shame in asking for support.",
        }
        
        # Find matching response
        for keywords, response in responses.items():
            if any(re.search(keyword.strip(), question_lower) for keyword in keywords.split("|")):
                return {
                    "answer": f"{response}\n\n**Disclaimer:** This is general health information, not medical advice. Please consult a healthcare professional for personalized guidance.",
                    "source_documents": []
                }
        
        # Default response if no keywords match
        return {
            "answer": "I can provide general health information about topics like diabetes, heart health, hypertension, asthma, diet, exercise, and mental health. However, for specific medical questions or conditions, I strongly recommend consulting with a qualified healthcare professional who can provide personalized advice based on your individual situation.\n\n**Disclaimer:** This is not medical advice. Please consult a healthcare professional.",
            "source_documents": []
        }
    
    def query(self, question: str) -> Dict:
        """Query the RAG system with a medical question - never crashes, always returns a response"""
        # Use keyword fallback if configured or if QA chain is not available
        if self.use_keyword_fallback or not self.qa_chain:
            return self._keyword_based_response(question)
        
        try:
            result = self.qa_chain({"query": question})
            
            return {
                "answer": result["result"],
                "source_documents": [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }
                    for doc in result["source_documents"]
                ]
            }
        except Exception as e:
            print(f"Query with LLM failed: {e}, falling back to keyword-based response")
            # Fallback to keyword-based response instead of crashing
            return self._keyword_based_response(question)
    
    def add_documents(self, documents: List[str]):
        """Add new documents to the knowledge base"""
        if not self.vectorstore:
            print("Vector store not initialized, cannot add documents")
            return
            
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            
            for doc in documents:
                chunks = text_splitter.split_text(doc)
                self.vectorstore.add_texts(chunks)
            
            self.vectorstore.persist()
        except Exception as e:
            print(f"Failed to add documents: {e}")

