from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from typing import List, Dict
import os
from app.core.config import settings

class MedicalRAGSystem:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.vectorstore = None
        self.qa_chain = None
        self.llm = OpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
        
    def initialize_vectorstore(self, documents: List[str] = None):
        """Initialize ChromaDB vector store with medical documents"""
        persist_dir = settings.CHROMA_PERSIST_DIR
        
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
        self.vectorstore.persist()
    
    def setup_qa_chain(self):
        """Setup RAG chain for medical queries"""
        if not self.vectorstore:
            self.initialize_vectorstore()
        
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
    
    def query(self, question: str) -> Dict:
        """Query the RAG system with a medical question"""
        if not self.qa_chain:
            self.setup_qa_chain()
        
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
    
    def add_documents(self, documents: List[str]):
        """Add new documents to the knowledge base"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        for doc in documents:
            chunks = text_splitter.split_text(doc)
            self.vectorstore.add_texts(chunks)
        
        self.vectorstore.persist()
