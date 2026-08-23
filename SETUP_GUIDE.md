# Setup Guide - AI Healthcare Assistant

## Prerequisites Installation

### 1. Python Environment
```bash
# Install Python 3.9+ from python.org

# Create virtual environment
cd MajorProject
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Node.js Environment
```bash
# Install Node.js 18+ from nodejs.org

# Verify installation
node --version
npm --version
```

### 3. MongoDB
```bash
# Download and install MongoDB from mongodb.com

# Start MongoDB service
# On Windows: Run as service or use mongod command
# On macOS: brew services start mongodb-community
# On Linux: sudo systemctl start mongod
```

### 4. Redis
```bash
# Download Redis from redis.io

# Start Redis server
redis-server
```

### 5. Tesseract OCR
```bash
# Windows: Download installer from github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend
pip install -r ../requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy example environment file
cp ../.env.example ../.env

# Edit .env with your actual values:
# - OPENAI_API_KEY: Get from platform.openai.com
# - SECRET_KEY: Generate a random string
# - MONGODB_URI: Your MongoDB connection string
# - REDIS_URL: Your Redis connection string
```

### 3. Download NLP Models
```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# The HuggingFace models will be downloaded automatically on first use
```

### 4. Train Disease Prediction Model (Optional)
```bash
cd backend
python -m app.models.train_disease_model
```

### 5. Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at http://localhost:8000

API Documentation: http://localhost:8000/docs

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

Frontend will be available at http://localhost:3000

## Initial Knowledge Base Setup

The RAG system needs medical knowledge. The sample file is provided at:
`data/sample_medical_knowledge.txt`

To add more knowledge:
1. Add medical text files to `data/medical_knowledge/`
2. The system will automatically index them

## Testing the Application

### 1. Register a User
- Navigate to http://localhost:3000/register
- Fill in registration details
- Submit the form

### 2. Login
- Navigate to http://localhost:3000/login
- Enter your credentials
- Access the dashboard

### 3. Test Features

**Medical Reports:**
- Go to Medical Reports page
- Upload a medical report image or enter text
- View the AI analysis

**Disease Prediction:**
- Go to Disease Prediction page
- Fill in health parameters
- Get AI-powered risk assessment

**Health Chat:**
- Go to Health Chat page
- Ask health-related questions
- Get AI responses with medical sources

**Recommendations:**
- Go to Recommendations page
- View personalized health suggestions
- Update your health profile for better recommendations

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
# On Windows: Check Services
# On macOS/Linux: sudo systemctl status mongod

# Start MongoDB if not running
# On Windows: net start MongoDB
# On macOS: brew services start mongodb-community
# On Linux: sudo systemctl start mongod
```

### Redis Connection Issues
```bash
# Start Redis server
redis-server

# Test connection
redis-cli ping
```

### Port Already in Use
```bash
# Change backend port (default 8000)
python -m uvicorn app.main:app --port 8001

# Change frontend port (default 3000)
# Edit vite.config.js and change server.port
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

## Production Deployment

### Backend
```bash
# Use gunicorn instead of uvicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or use Docker (Dockerfile recommended)
docker build -t healthcare-backend .
docker run -p 8000:8000 healthcare-backend
```

### Frontend
```bash
# Build for production
npm run build

# Serve with nginx or any static file server
```

## Security Notes

1. Never commit `.env` file to version control
2. Use strong SECRET_KEY in production
3. Enable HTTPS in production
4. Implement rate limiting on API endpoints
5. Regularly update dependencies
6. Use environment-specific configurations

## License

MIT License - See LICENSE file for details
