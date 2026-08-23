# AI-Powered Multi-Disease Healthcare Assistant

A comprehensive healthcare platform using Deep Learning, Machine Learning, RAG (Retrieval-Augmented Generation), and Medical Report Analysis.

## Features

- **RAG System**: Intelligent medical knowledge retrieval using LangChain and ChromaDB
- **Medical Report Analysis**: OCR-based document analysis with NLP processing
- **Disease Prediction**: Deep learning models for multi-disease risk assessment
- **Personalized Recommendations**: ML-driven health suggestions based on user data
- **Chat Interface**: AI-powered health assistant for medical queries
- **Dashboard**: Comprehensive health monitoring and tracking

## Tech Stack

### Backend
- FastAPI (Python web framework)
- PyTorch (Deep learning)
- Scikit-learn (Machine learning)
- LangChain (RAG framework)
- ChromaDB (Vector database)
- MongoDB (Data storage)
- Redis (Caching)
- Celery (Task queue)

### Frontend
- React (UI framework)
- TailwindCSS (Styling)
- shadcn/ui (Components)
- Lucide (Icons)

### ML/DL Models
- Disease prediction using neural networks
- Medical text classification with transformers
- Image analysis for medical reports
- Recommendation engine using collaborative filtering

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB
- Redis
- Tesseract OCR

### Backend Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Start backend server:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

## Project Structure

```
MajorProject/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core functionality
│   │   ├── models/           # ML/DL models
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utilities
├── frontend/                 # React application
├── data/                     # Training data and knowledge base
└── notebooks/                # Jupyter notebooks for development
```

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/medical/upload` - Upload medical reports
- `POST /api/medical/analyze` - Analyze medical reports
- `POST /api/predict/disease` - Disease prediction
- `POST /api/chat/query` - Health chat query
- `GET /api/recommendations` - Personalized recommendations

## Model Training

Train disease prediction models:
```bash
cd backend
python -m app.models.train_disease_model
```

## License

MIT License
