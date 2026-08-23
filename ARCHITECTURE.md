# Architecture Documentation

## System Overview

The AI-Powered Healthcare Assistant is a full-stack application consisting of:

- **Backend**: FastAPI-based REST API with ML/DL models
- **Frontend**: React-based single-page application
- **Databases**: MongoDB (document storage), Redis (caching), ChromaDB (vector storage)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                   │
│  Dashboard | Medical Reports | Prediction | Chat | Recs  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│              Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Layer (auth, medical, prediction, chat)     │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Services Layer                                  │  │
│  │  - Medical Report Analyzer (OCR + NLP)          │  │
│  │  - Recommendation Engine (ML)                    │  │
│  │  - RAG System (LangChain + ChromaDB)            │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ML/DL Models                                     │  │
│  │  - Disease Prediction (PyTorch Neural Network)   │  │
│  │  - Medical NER (Transformers)                    │  │
│  │  - Embeddings (Sentence Transformers)            │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌───▼────────┐
│   MongoDB    │ │  Redis  │ │  ChromaDB  │
│  (User Data) │ │ (Cache) │ │ (Vectors)  │
└──────────────┘ └─────────┘ └────────────┘
```

## Component Details

### Backend Components

#### 1. API Layer (`app/api/`)
- **auth.py**: User authentication and authorization
- **medical.py**: Medical report upload and analysis
- **prediction.py**: Disease risk prediction
- **chat.py**: RAG-based health chat
- **recommendations.py**: Personalized health recommendations

#### 2. Core Layer (`app/core/`)
- **config.py**: Application configuration and settings
- **database.py**: Database connections (MongoDB, Redis)
- **security.py**: JWT authentication and password hashing

#### 3. Models Layer (`app/models/`)
- **disease_model.py**: PyTorch neural network for disease prediction
- **rag_system.py**: LangChain-based RAG implementation
- **train_disease_model.py**: Model training script

#### 4. Services Layer (`app/services/`)
- **medical_report_analyzer.py**: OCR and NLP for medical reports
- **recommendation_engine.py**: ML-based recommendation system

### Frontend Components

#### 1. Pages (`src/pages/`)
- **Login.jsx**: User authentication
- **Register.jsx**: User registration
- **Dashboard.jsx**: Main dashboard with stats
- **MedicalReports.jsx**: Report upload and analysis
- **DiseasePrediction.jsx**: Health risk assessment
- **HealthChat.jsx**: AI health assistant chat
- **Recommendations.jsx**: Personalized suggestions

#### 2. Components (`src/components/`)
- **Layout.jsx**: Main application layout with navigation

#### 3. Context (`src/contexts/`)
- **AuthContext.jsx**: Authentication state management

#### 4. Utilities (`src/utils/`)
- **api.js**: Axios API client with interceptors
- **cn.js**: Tailwind CSS class utility

## Data Flow

### Medical Report Analysis Flow
```
1. User uploads report → Frontend
2. File sent to /api/medical/upload → Backend
3. OCR extraction (Tesseract) → MedicalReportAnalyzer
4. NLP processing (spaCy, Transformers) → Entity extraction
5. Analysis stored in MongoDB → Response to frontend
6. Results displayed → Frontend
```

### Disease Prediction Flow
```
1. User enters health data → Frontend
2. Data sent to /api/predict/disease → Backend
3. Feature extraction → DiseasePredictor
4. Model inference (PyTorch) → Risk assessment
5. Results stored in MongoDB → Response to frontend
6. Visualization → Frontend
```

### RAG Chat Flow
```
1. User asks question → Frontend
2. Query sent to /api/chat/query → Backend
3. Query embedding (Sentence Transformers) → RAG System
4. Vector search (ChromaDB) → Relevant documents
5. Context + Query → LLM (OpenAI) → Answer
6. Response with sources → Frontend
```

### Recommendation Flow
```
1. User profile loaded → Backend
2. Profile analysis → Recommendation Engine
3. Similar user matching (TF-IDF) → User clustering
4. Rule-based + ML recommendations → Personalized list
5. Response → Frontend
6. Display with priorities → Frontend
```

## Database Schema

### MongoDB Collections

#### users
```json
{
  "_id": ObjectId,
  "email": String,
  "password": String (hashed),
  "full_name": String,
  "age": Number,
  "gender": String,
  "conditions": [String],
  "medications": [String],
  "health_profile": {
    "lifestyle": Object,
    "preferences": Object
  },
  "created_at": DateTime
}
```

#### medical_reports
```json
{
  "_id": ObjectId,
  "user_id": String,
  "filename": String,
  "file_path": String,
  "text_input": String (optional),
  "analysis": {
    "extracted_text": String,
    "medical_entities": Object,
    "sentiment": String,
    "summary": String,
    "recommendations": [String]
  },
  "uploaded_at": DateTime,
  "analyzed_at": DateTime
}
```

#### predictions
```json
{
  "_id": ObjectId,
  "user_id": String,
  "health_data": Object,
  "prediction": {
    "predicted_disease": String,
    "confidence": Number,
    "all_probabilities": Object,
    "risk_factors": [String],
    "recommendations": [String]
  },
  "created_at": DateTime
}
```

#### chat_history
```json
{
  "_id": ObjectId,
  "user_id": String,
  "question": String,
  "answer": String,
  "source_documents": [Object],
  "timestamp": DateTime
}
```

## ML/DL Models

### Disease Prediction Model
- **Architecture**: 3-layer Neural Network
- **Input**: 20 health features
- **Output**: 10 disease probabilities
- **Framework**: PyTorch
- **Training**: Synthetic data generation + supervised learning

### Medical NER Model
- **Model**: BERT-based (samrawat/bert-base-uncased-medical-ner)
- **Task**: Named Entity Recognition
- **Entities**: Diseases, Medications, Symptoms
- **Framework**: HuggingFace Transformers

### Embedding Model
- **Model**: all-MiniLM-L6-v2
- **Task**: Sentence embeddings for RAG
- **Framework**: Sentence Transformers
- **Dimension**: 384

## Security Considerations

1. **Authentication**: JWT-based stateless authentication
2. **Password Security**: Bcrypt hashing with salt
3. **API Security**: CORS configuration, rate limiting (recommended)
4. **Data Privacy**: Medical data encryption at rest (recommended)
5. **Input Validation**: Pydantic models for request validation

## Scalability Considerations

1. **Horizontal Scaling**: Stateless API design allows multiple instances
2. **Caching**: Redis for frequently accessed data
3. **Database Indexing**: MongoDB indexes on user_id, timestamps
4. **Async Operations**: FastAPI async/await for I/O operations
5. **Vector Database**: ChromaDB for efficient similarity search

## Future Enhancements

1. **Real-time Notifications**: WebSocket integration
2. **Mobile App**: React Native or Flutter
3. **Advanced Analytics**: Time-series health tracking
4. **Integration**: EHR system integration (HL7/FHIR)
5. **Multi-language**: Support for multiple languages
6. **Voice Interface**: Speech-to-text for health queries
7. **Wearable Integration**: Apple Health, Google Fit integration
