# MediPredict - AI-Powered Healthcare Assistant

## 📋 Project Overview

**MediPredict** is an academic healthcare assistant that provides AI-powered medical information, disease prediction using machine learning, and personalized health recommendations. The application uses real medical data from reputable sources and integrates with OpenAI's GPT-3.5-turbo for intelligent responses.

### **Key Features:**
- ✅ **ML-Powered Disease Prediction** - Uses trained ML models for diabetes, heart disease, and hypertension
- ✅ **AI-Powered Health Chatbot** - RAG system with OpenAI GPT-3.5-turbo (or medical knowledge base fallback)
- ✅ **Medical Report Analysis** - NLP text analysis with ICD-10 codes
- ✅ **Personalized Health Recommendations** - Age-based screening guidelines
- ✅ **Real-Time Health Dashboard** - Highcharts visualizations
- ✅ **User Authentication** - JWT-based
- ✅ **Database Persistence** - PostgreSQL
- ✅ **Evidence-Based Medical Data** - From WHO, CDC, Mayo Clinic, NIH, AHA

---

## 🛠️ Technology Stack

### **Backend:**
- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn 0.24.0
- **Database:** PostgreSQL (asyncpg 0.29.0)
- **Authentication:** JWT (python-jose, passlib)
- **AI Integration:** OpenAI GPT-3.5-turbo
- **ML Library:** scikit-learn 1.3.2
- **Data Processing:** pandas 2.1.4, numpy 1.26.2
- **Medical NLP:** Custom regex-based extraction
- **Data Validation:** Pydantic 2.5.0

### **Frontend:**
- **Framework:** React with Vite
- **Charts:** Highcharts (highcharts-react-official)
- **HTTP Client:** Axios
- **Routing:** React Router
- **UI Components:** Lucide Icons
- **State Management:** React Context API
- **Build Tool:** Vite 5.4.21

### **Data Storage:**
- **Production:** PostgreSQL (Render free tier)
- **Local:** PostgreSQL 16
- **Fallback:** In-memory (demo mode)

### **ML/AI:**
- **ML Models:** scikit-learn (Random Forest, Logistic Regression)
- **LLM:** OpenAI GPT-3.5-turbo
- **RAG System:** Custom implementation with medical knowledge base
- **Model Training:** Public datasets (Pima Indians Diabetes, Cleveland Heart Disease)

---

## 📁 Project Structure

```
MajorProject/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── chat.py          # AI chatbot (RAG system)
│   │   │   ├── medical.py       # Medical report analysis
│   │   │   ├── prediction.py    # ML-based disease prediction
│   │   │   └── recommendations.py # Health recommendations
│   │   ├── core/
│   │   │   ├── config.py        # Configuration
│   │   │   ├── database.py      # PostgreSQL connection
│   │   │   └── security.py      # JWT authentication
│   │   ├── data/
│   │   │   ├── medical_knowledge.py  # Real medical data
│   │   │   └── medical_reports.py    # ICD codes, templates
│   │   ├── models/
│   │   │   ├── rag_system.py    # RAG implementation
│   │   │   └── ml_models.py      # ML model loader
│   │   └── main.py              # FastAPI application
│   ├── models/                   # Trained ML models
│   │   ├── diabetes_model.pkl
│   │   ├── heart_disease_model.pkl
│   │   ├── hypertension_model.pkl
│   │   └── scalers, features.pkl
│   ├── train_models.py          # ML model training script
│   ├── requirements.txt
│   └── .env                    # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── charts/          # Highcharts components
│   │   │   ├── Layout.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   └── ErrorBoundary.jsx
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DiseasePrediction.jsx
│   │   │   ├── MedicalReports.jsx
│   │   │   ├── HealthChat.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── utils/
│   │   │   ├── api.js
│   │   │   └── errorHandler.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── Dockerfile                   # For Render deployment
├── render.yaml                  # Render configuration
├── SETUP_GUIDE.md               # Setup instructions
└── PROJECT_DOCUMENTATION.md      # This file
```

---

## 🗄️ PostgreSQL Setup Guide

### **Step 1: Install PostgreSQL**

1. **Download PostgreSQL** for Windows:
   - Go to: https://www.postgresql.org/download/windows/
   - Download the latest version (PostgreSQL 16.x)
   - Run the installer

2. **During Installation:**
   - **Password**: Set a password (remember it! e.g., `KAVYA`)
   - **Port**: Keep default `5432`
   - **Components**: Select PostgreSQL Server and pgAdmin 4
   - **Stack Builder**: Optional (can skip)

3. **Complete Installation:**
   - Wait for installation to finish
   - Click "Finish"

### **Step 2: Create Database**

**Option A: Using pgAdmin (Recommended):**
1. Open **pgAdmin 4** from Start menu
2. Click **"Servers"** → **"PostgreSQL 16"**
3. Enter your PostgreSQL password
4. Right-click on **"Databases"** → **"Create"** → **"Database"**
5. **Database name**: `healthcare_db`
6. Click **"Save"**

**Option B: Using SQL Shell:**
1. Open **SQL Shell (psql)** from Start menu
2. Enter your PostgreSQL password
3. Type: `CREATE DATABASE healthcare_db;`
4. Press Enter
5. Type: `\q` to exit

### **Step 3: Reset PostgreSQL Password (if needed)**

If you forgot your password:
1. Open **SQL Shell (psql)**
2. Enter current password
3. Type: `ALTER USER postgres WITH PASSWORD 'your_new_password';`
4. Press Enter
5. Type: `\q` to exit

---

## ⚙️ Backend Configuration

### **Step 1: Configure Environment Variables**

1. Navigate to: `C:\Users\girig\Desktop\MajorProject\backend`
2. Create or edit `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/healthcare_db
```

3. **Replace:**
   - `your-openai-api-key-here` with your OpenAI API key (optional - see Chatbot section)
   - `YOUR_PASSWORD` with your PostgreSQL password

### **Step 2: Install Backend Dependencies**

```bash
cd C:\Users\girig\Desktop\MajorProject\backend
pip install -r requirements.txt
```

### **Step 3: Train ML Models (First Time Only)**

```bash
cd C:\Users\girig\Desktop\MajorProject\backend
python train_models.py
```

This will:
- Download public medical datasets (Pima Indians Diabetes, Cleveland Heart Disease)
- Train 3 ML models (diabetes, heart disease, hypertension)
- Save models to `backend/models/` directory
- Display model accuracies

### **Step 4: Start Backend**

```bash
cd C:\Users\girig\Desktop\MajorProject\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: PostgreSQL connection pool created successfully
INFO: ML models loaded successfully
INFO: RAG system initialized with OpenAI API
INFO: Application startup complete
```

---

## 🎨 Frontend Setup

### **Step 1: Install Frontend Dependencies**

```bash
cd C:\Users\girig\Desktop\MajorProject\frontend
npm install
```

### **Step 2: Start Frontend**

```bash
cd C:\Users\girig\Desktop\MajorProject\frontend
npm run dev
```

**Expected Output:**
```
VITE v5.4.21 ready in xxx ms
➜ Local: http://localhost:3005/
```

### **Step 3: Access Application**

Open your browser and go to: **http://localhost:3005**

---

## 🧪 Feature-by-Feature Documentation

### **1. User Authentication**

**Purpose:** To authenticate users and save their health data securely using JWT tokens.

**How It Works:**
- User registers with email/password
- Password is hashed using bcrypt (industry standard)
- JWT token generated upon login
- Token stored in localStorage for session management
- Protected routes require authentication

**Technology:**
- FastAPI endpoints
- JWT (python-jose)
- Passlib bcrypt for password hashing
- PostgreSQL for user storage

**Data Used:**
- User data (email, password hash, name, age, gender)
- Stored in PostgreSQL `users` table

**Data Source:** 
- User-provided during registration

---

### **2. ML-Powered Disease Prediction**

**Purpose:** To predict disease risk using machine learning models trained on real medical data.

**How It Works:**
- Uses 3 trained ML models:
  - **Diabetes Model**: Random Forest trained on Pima Indians Diabetes dataset
  - **Heart Disease Model**: Random Forest trained on Cleveland Heart Disease dataset
  - **Hypertension Model**: Logistic Regression trained on synthetic health data
- Accepts health parameters (age, BMI, blood pressure, glucose, cholesterol, etc.)
- Scales features using StandardScaler
- Returns probability-based risk assessment
- Generates personalized recommendations

**Technology:**
- scikit-learn (Random Forest, Logistic Regression)
- pandas (data handling)
- numpy (numerical computing)
- joblib (model serialization)

**Data Used:**
- **Pima Indians Diabetes Dataset** (UCI ML Repository)
  - 768 samples
  - 8 features: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age
  - Target: Diabetes diagnosis (0 or 1)
  - Model Accuracy: 72.08%

- **Cleveland Heart Disease Dataset** (UCI ML Repository)
  - 303 samples
  - 14 features: age, sex, chest pain type, resting BP, cholesterol, fasting blood sugar, resting ECG, max heart rate, exercise angina, ST depression, ST slope, major vessels, thalassemia
  - Target: Heart disease (0 or 1)
  - Model Accuracy: 55.74%

- **Synthetic Health Dataset** (for hypertension)
  - 500 samples
  - 8 features: age, BMI, systolic BP, diastolic BP, cholesterol, physical activity, smoking, family history
  - Target: Hypertension risk (0 or 1)
  - Model Accuracy: 64.00%

**Data Sources:**
- **Pima Indians Diabetes**: https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
- **Cleveland Heart Disease**: https://raw.githubusercontent.com/plotly/datasets/master/heart.csv
- **Synthetic**: Generated for hypertension (no public dataset available)

**Where Data From:**
- UCI Machine Learning Repository (public datasets)
- National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)
- National Heart, Lung, and Blood Institute (NHLBI)

**Model Files:**
- `backend/models/diabetes_model.pkl` - Trained Random Forest model
- `backend/models/heart_disease_model.pkl` - Trained Random Forest model
- `backend/models/hypertension_model.pkl` - Trained Logistic Regression model
- `backend/models/diabetes_scaler.pkl` - Feature scaler for diabetes
- `backend/models/heart_disease_scaler.pkl` - Feature scaler for heart disease
- `backend/models/hypertension_scaler.pkl` - Feature scaler for hypertension
- `backend/models/diabetes_features.pkl` - Feature names for diabetes
- `backend/models/heart_disease_features.pkl` - Feature names for heart disease
- `backend/models/hypertension_features.pkl` - Feature names for hypertension

---

### **3. Medical Report Analysis**

**Purpose:** To analyze medical reports, extract lab values, provide clinical interpretation, and suggest ICD-10 codes.

**How It Works:**
- Accepts medical text or uploaded files
- Uses regex/NLP to extract lab values (glucose, cholesterol, blood pressure)
- Matches patterns against medical terminology
- Suggests ICD-10 codes based on detected conditions
- Provides clinical significance interpretation
- Uses real medical report templates

**Technology:**
- Regular expressions (regex) for pattern matching
- Custom NLP for medical entity extraction
- ICD-10 classification system

**Data Used:**
- **ICD-10 Codes**: International Classification of Diseases
  - Diabetes: E10 (Type 1), E11 (Type 2), R73.03 (Prediabetes)
  - Hypertension: I10 (Essential), I15 (Secondary)
  - Cardiovascular: I20 (Angina), I21-I22 (Heart attack), I50 (Heart failure)
  - Obesity: E66.0-66.2 (BMI categories)

- **Medical Terminology**: Real clinical lab value ranges
  - Blood glucose: Normal <100, Prediabetes 100-125, Diabetes ≥126 mg/dL
  - Cholesterol: Normal <200, Borderline 200-239, High ≥240 mg/dL
  - Blood pressure: Normal <120/80, Elevated 120-129/<80, Stage 1 130-139/80-89, Stage 2 140+/90+

- **Medical Report Templates**: Lab reports, radiology reports, progress notes
- **Sample Clinical Cases**: Diabetes, Hypertension, Cardiovascular cases

**Data Sources:**
- **ICD-10 Classification**: WHO ICD-10 (https://icd.who.int/browse10/2019/en)
- **Clinical Lab Value Ranges**: Mayo Clinic, NIH, CDC
- **Medical Terminology**: Clinical practice guidelines

**Where Data From:**
- World Health Organization (WHO)
- National Institutes of Health (NIH)
- Mayo Clinic
- Centers for Disease Control and Prevention (CDC)

---

### **4. AI-Powered Health Chatbot**

**Purpose:** To provide AI-powered medical information and health guidance using retrieval-augmented generation (RAG).

**How It Works:**
- **RAG System**: Retrieves relevant medical documents from knowledge base
- **Retrieval**: Keyword-based search through medical knowledge base
- **Generation**: Uses OpenAI GPT-3.5-turbo for AI responses (if API key available)
- **Fallback**: Uses medical knowledge base with specific information if API unavailable
- **Context-Aware**: Responses based on retrieved medical documents
- **Evidence-Based**: All information from reputable medical sources

**Technology:**
- OpenAI GPT-3.5-turbo (if credits available)
- Medical knowledge base (keyword matching)
- Custom RAG implementation

**Data Used:**
- **Medical Knowledge Base**: Comprehensive medical information
  - **Diabetes**: Symptoms, risk factors, prevention, treatment, complications
  - **Hypertension**: Symptoms, risk factors, prevention, treatment, target values
  - **Heart Disease**: Symptoms, risk factors, prevention, treatment, diet recommendations
  - **General Health**: Nutrition, exercise, sleep, hydration guidelines
  - **Lab Values**: Blood glucose, cholesterol, blood pressure reference ranges
  - **Fever**: Causes, when to see doctor, home care, temperature ranges
  - **Back Pain**: Causes, prevention, when to see doctor

**Data Sources:**
- **World Health Organization (WHO)** - Global health guidelines
- **Centers for Disease Control and Prevention (CDC)** - Public health data
- **Mayo Clinic** - Clinical practice guidelines
- **National Institutes of Health (NIH)** - Medical research
- **American Heart Association (AHA)** - Cardiovascular guidelines

**Where Data From:**
- WHO health topics: https://www.who.int/health-topics
- CDC health data: https://www.cdc.gov/
- Mayo Clinic medical information: https://www.mayoclinic.org/diseases-conditions
- NIH medical research: https://www.niddk.nih.gov/health-information
- AHA cardiovascular guidelines: https://www.heart.org/en/health-topics/

**Why OpenAI API Key Not Available:**
- OpenAI changed policy - no longer provides free credits to new accounts
- Requires manual credit addition ($5-10 minimum)
- Without credits, API returns "429 - No credits remaining" error
- Current solution uses comprehensive medical knowledge base
- With credits, would use GPT-3.5-turbo for dynamic AI responses

**Current Behavior:**
- ✅ Provides specific medical information (fever, back pain, diabetes, etc.)
- ✅ Uses real medical data from reputable sources
- ✅ Evidence-based and medically accurate
- ❌ Not dynamic AI-generated (requires OpenAI credits)

**Future with Credits:**
- ✅ Would use GPT-3.5-turbo for dynamic AI responses
- ✅ Each response would be unique and contextual
- ✅ More conversational and personalized
- Still based on medical knowledge base for accuracy

---

### **5. Health Recommendations**

**Purpose:** To provide age-appropriate screening guidelines and personalized health recommendations.

**How It Works:**
- Age-based screening guidelines from USPSTF
- Lifestyle recommendations based on health profile
- Personalized based on risk factors
- Evidence-based clinical practice guidelines

**Technology:**
- Age-based rule system
- USPSTF guidelines database
- Clinical practice guidelines

**Data Used:**
- **USPSTF Screening Guidelines**: Age-appropriate health screenings
  - **18-39**: Blood pressure, cholesterol, BMI, cancer screenings
  - **40-49**: Mammograms, colon cancer, prostate screening
  - **50-64**: Bone density, lung cancer, shingles vaccine
  - **65+**: Comprehensive screening, vaccines, hearing tests

- **Lifestyle Recommendations**:
  - **Diet**: Mediterranean diet, DASH diet, nutritional guidelines
  - **Exercise**: WHO guidelines (150 min/week moderate activity)
  - **Sleep**: NIH guidelines (7-9 hours for adults)
  - **Stress Management**: Meditation, yoga, relaxation techniques
  - **Hydration**: Water intake guidelines

**Data Sources:**
- **US Preventive Services Task Force (USPSTF)** - Screening recommendations
- **World Health Organization (WHO)** - Exercise guidelines
- **National Institutes of Health (NIH)** - Sleep guidelines
- **American Heart Association (AHA)** - Diet guidelines

**Where Data From:**
- USPSTF: https://www.uspreventiveservicestaskforce.org/
- WHO exercise: https://www.who.int/dietphysicalactivity/pa
- NIH sleep: https://www.nhlbi.nih.gov/health/sleep

---

### **6. Dashboard**

**Purpose:** To visualize health data, trends, and predictions in an intuitive interface.

**How It Works:**
- Displays health metrics and risk assessments
- Shows disease prediction history
- Visualizes trends using Highcharts
- Interactive data exploration

**Technology:**
- Highcharts (highcharts-react-official)
- React state management
- Data visualization

**Data Used:**
- User prediction history from PostgreSQL
- Risk assessment trends
- Health metrics over time

**Data Source:**
- PostgreSQL database (user predictions table)

---

## 📊 Data Sources Summary

### **Primary Data Sources:**

| Feature | Data Source | Type | Dataset/Information | Where From |
|---------|-------------|------|-------------------|------------|
| **Disease Prediction (ML)** | Pima Indians Diabetes | Public dataset (768 samples, 8 features) | UCI ML Repository |
| **Disease Prediction (ML)** | Cleveland Heart Disease | Public dataset (303 samples, 14 features) | UCI ML Repository |
| **Disease Prediction (ML)** | Synthetic Health Dataset | Synthetic (500 samples, 8 features) | Generated for hypertension |
| **Medical Reports** | ICD-10 Classification | Medical coding system | WHO ICD-10 |
| **Medical Reports** | Lab Value Ranges | Clinical reference ranges | Mayo Clinic, NIH, CDC |
| **Medical Reports** | Medical Terminology | Clinical terminology | Clinical practice guidelines |
| **Chatbot** | Medical Knowledge Base | Diabetes, hypertension, heart disease, general health | WHO, CDC, Mayo Clinic, NIH, AHA |
| **Chatbot** | Fever/Back Pain Info | Symptoms, causes, treatment | Medical guidelines |
| **Recommendations** | USPSTF Guidelines | Age-based screening | USPSTF |
| **Recommendations** | Lifestyle Guidelines | Diet, exercise, sleep, stress | WHO, NIH, AHA |

### **Data Source URLs:**

- **Pima Indians Diabetes**: https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv
- **Cleveland Heart Disease**: https://raw.githubusercontent.com/plotly/datasets/master/heart.csv
- **WHO ICD-10**: https://icd.who.int/browse10/2019/en
- **WHO Health Topics**: https://www.who.int/health-topics
- **CDC Health Data**: https://www.cdc.gov/
- **Mayo Clinic**: https://www.mayoclinic.org/diseases-conditions
- **NIH Medical Research**: https://www.niddk.nih.gov/health-information
- **AHA Guidelines**: https://www.heart.org/en/health-topics/
- **USPSTF**: https://www.uspreventiveservicestaskforce.org/

---

## 🔍 Database Schema

### **PostgreSQL Tables:**

1. **users**
   - id (SERIAL PRIMARY KEY)
   - email (VARCHAR(255) UNIQUE NOT NULL)
   - password (VARCHAR(255) NOT NULL)
   - full_name (VARCHAR(255))
   - age (INTEGER)
   - gender (VARCHAR(50))
   - created_at (TIMESTAMP)
   - conditions (TEXT[])
   - medications (TEXT[])
   - health_profile (JSONB)

2. **medical_reports**
   - id (   SERIAL PRIMARY KEY)
   - user_id (INTEGER REFERENCES users(id))
   - filename (VARCHAR(255))
   - file_path (TEXT)
   - text_input (TEXT)
   - analysis (JSONB)
   - uploaded_at (TIMESTAMP)
   - analyzed_at (TIMESTAMP)

3. **predictions**
   - id (SERIAL PRIMARY KEY)
   - user_id (INTEGER REFERENCES users(id))
   - health_data (JSONB)
   - predicted_disease (VARCHAR(255))
   - confidence (FLOAT)
   - risk_factors (TEXT[])
   - recommendations (TEXT[])
   - all_probabilities (JSONB)
   - created_at (TIMESTAMP)

4. **chat_history**
   - id (SERIAL PRIMARY KEY)
   - user_id (INTEGER REFERENCES users(id))
   - question (TEXT)
   - answer (TEXT)
   - source_documents (TEXT[])
   - timestamp (TIMESTAMP)

---

## 🎯 Complete Setup Workflow

### **Step 1: Install PostgreSQL**
- Download from: https://www.postgresql.org/download/windows/
- Install with password (e.g., `KAVYA`)
- Create database: `healthcare_db`

### **Step 2: Configure Backend**
- Navigate to `backend/` directory
- Edit `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=postgresql://postgres:KAVYA@localhost:5432/healthcare_db
```

### **Step 3: Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### **Step 4: Train ML Models**
```bash
cd backend
python train_models.py
```

### **Step 5: Start Backend**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 6: Start Frontend**
```bash
cd frontend
npm install
npm run dev
```

### **Step 7: Access Application**
- Open browser: http://localhost:3005
- Register and login
- Test all features

---

## 🧪 Testing Each Feature

### **1. User Registration & Login**
- **Purpose**: Test authentication with PostgreSQL
- **Data Stored**: User information in PostgreSQL `users` table
- **Verify in pgAdmin**: View `users` table → All Rows

### **2. Disease Prediction (ML-Based)**
- **Purpose**: Test ML models trained on real medical data
- **Models Used**: Diabetes (Random Forest), Heart Disease (Random Forest), Hypertension (Logistic Regression)
- **Data Sources**: Pima Indians Dataset, Cleveland Heart Disease Dataset
- **Accuracy**: Diabetes 72.08%, Heart Disease 55.74%, Hypertension 64.00%
- **Data Stored**: Predictions in PostgreSQL `predictions` table
- **Verify in pgAdmin**: View `predictions` table → All Rows

### **3. Medical Report Analysis**
- **Purpose**: Test NLP analysis with ICD-10 codes
- **Data Used**: ICD-10 codes, lab value ranges, medical terminology
- **Data Sources**: WHO ICD-10, Mayo Clinic, NIH
- **Data Stored**: Reports in PostgreSQL `medical_reports` table
- **Verify in pgAdmin**: View `medical_reports` table → All Rows

### **4. Health Chatbot**
- **Purpose**: Test medical information retrieval
- **Data Used**: Medical knowledge base (WHO, CDC, Mayo Clinic, NIH, AHA)
- **Data Sources**: WHO, CDC, Mayo Clinic, NIH, AHA
- **Data Stored**: Chat history in PostgreSQL `chat_history` table
- **Verify in pgAdmin**: View `chat_history` table → All Rows

### **5. Health Recommendations**
- **Purpose**: Test age-based screening guidelines
- **Data Used**: USPSTF guidelines, lifestyle recommendations
- **Data Sources**: USPSTF, WHO, NIH, AHA
- **No database storage** (real-time calculation)

### **6. Dashboard**
- **Purpose**: Visualize health data and trends
- **Data Used**: Prediction history from PostgreSQL
- **Data Source**: PostgreSQL `predictions` table
- **Verify in pgAdmin**: View `predictions` table → All Rows

---

## 📊 ML Model Details

### **Diabetes Prediction Model**
- **Algorithm**: Random Forest Classifier
- **Dataset**: Pima Indians Diabetes (UCI ML Repository)
- **Samples**: 768
- **Features**: 8 (Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Diabetes Pedigree Function, Age)
- **Target**: Diabetes diagnosis (0 or 1)
- **Accuracy**: 72.08%
- **Model File**: `backend/models/diabetes_model.pkl`
- **Training Command**: `python train_models.py`

### **Heart Disease Model**
- **Algorithm**: Random Forest Classifier
- **Dataset**: Cleveland Heart Disease (UCI ML Repository)
- **Samples**: 303
- **Features**: 14 (age, sex, chest pain type, resting BP, cholesterol, fasting blood sugar, resting ECG, max heart rate, exercise angina, ST depression, ST slope, major vessels, thalassemia)
- **Target**: Heart disease (0 or 1)
- **Accuracy**: 55.74%
- **Model File**: `backend/models/heart_disease_model.pkl`
- **Training Command**: `python train_models.py`

### **Hypertension Model**
- **Algorithm**: Logistic Regression
- **Dataset**: Synthetic health data (500 samples)
- **Features**: 8 (age, BMI, systolic BP, diastolic BP, cholesterol, physical activity, smoking, family history)
- **Target**: Hypertension risk (0 or 1)
- **Accuracy**: 64.00%
- **Model File**: `backend/models/hypertension_model.pkl`
- **Training Command**: `python train_models.py`

---

## 🔧 Troubleshooting

### **PostgreSQL Connection Failed**
**Error:** `PostgreSQL connection failed: password authentication failed`

**Solution:**
1. Verify password in `.env` matches PostgreSQL password
2. Reset PostgreSQL password using SQL Shell
3. Update `.env` with correct password
4. Restart backend

### **Backend Won't Start**
**Error:** `ModuleNotFoundError: No module named 'asyncpg'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### **ML Models Not Loading**
**Error:** ML models not loaded at startup

**Solution:**
```bash
cd backend
python train_models.py
```

### **Frontend Won't Start**
**Error:** Port already in use

**Solution:**
- Frontend will automatically try ports 3000-3005
- Check which port it starts on
- Access that URL (e.g., http://localhost:3005)

---

## 🎯 Application Summary

### **Features Using ML Models:**
- ✅ **Disease Prediction** - Uses 3 ML models (diabetes, heart disease, hypertension) trained on public medical datasets

### **Features Using Other Approaches:**
- ⚠️ **Chatbot** - Medical knowledge base + keyword matching (not ML)
- ⚠️ **Medical Reports** - Regex/NLP text analysis (not ML)
- ⚠️ **Recommendations** - Age-based guidelines (not ML)

### **Data Sources:**
- **ML Training**: UCI ML Repository (Pima Indians Diabetes, Cleveland Heart Disease)
- **Medical Knowledge**: WHO, CDC, Mayo Clinic, NIH, AHA
- **Clinical Guidelines**: USPSTF, ICD-10 classification
- **Lab Values**: Mayo Clinic, NIH, CDC reference ranges

### **Current Status:**
- ✅ ML models trained and integrated
- ✅ PostgreSQL connected and working
- ✅ Real medical data from reputable sources
- ✅ Evidence-based medical information
- ✅ User authentication working
- ✅ All features functional

---

## 📚 References & Citations

### **Primary Sources:**

1. **World Health Organization (WHO)**
   - Diabetes Guidelines: https://www.who.int/health-topics/diabetes
   - Hypertension Guidelines: https://www.who.int/health-topics/hypertension
   - Cardiovascular Disease: https://www.who.int/health-topics/cardiovascular-diseases

2. **Centers for Disease Control and Prevention (CDC)**
   - Diabetes: https://www.cdc.gov/diabetes
   - Heart Disease: https://www.cdc.gov/heartdisease
   - Nutrition: https://www.cdc.gov/nutrition

3. **Mayo Clinic**
   - Diabetes: https://www.mayoclinic.org/diseases-conditions/diabetes
   - Hypertension: https://www.mayoclinic.org/diseases-conditions/high-blood-pressure
   - Heart Disease: https://www.mayoclinic.org/diseases-conditions/heart-disease

4. **National Institutes of Health (NIH)**
   - Diabetes: https://www.niddk.nih.gov/health-information/diabetes
   - Heart Disease: https://www.nhlbi.nih.gov/health-topics/heart-disease

5. **American Heart Association (AHA)**
   - Blood Pressure: https://www.heart.org/en/health-topics/high-blood-pressure
   - Cholesterol: https://www.heart.org/en/health-topics/cholesterol
   - Heart Disease: https://www.heart.org/en/health-topics/heart-attack

6. **US Preventive Services Task Force (USPSTF)**
   - Screening Guidelines: https://www.uspreventiveservicestaskforce.org/

7. **UCI Machine Learning Repository**
   - Pima Indians Diabetes: https://archive.ics.uci.edu/ml/datasets/pima-indians-diabetes
   - Cleveland Heart Disease: https://archive.ics.uci.edu/ml/datasets/heart-disease

8. **ICD-10 Classification**
   - WHO ICD-10: https://icd.who.int/browse10/2019/en

---

## 🚀 Deployment Status

### **Local Development:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3005
- Database: PostgreSQL localhost:5432

### **Production (Pending):**
- Backend: Render (Docker deployment)
- Frontend: Served by backend (single URL)
- Database: Render PostgreSQL (free tier)
- URL: https://medipredict-backend.onrender.com

---

## 📄 License

This project is for academic and educational purposes only.

---

## 👥 Contributors

- **Development:** [Your Name]
- **Data Sources:** WHO, CDC, Mayo Clinic, NIH, AHA, USPSTF, UCI ML Repository
- **ML Models:** Trained on public medical datasets
- **AI Model:** OpenAI GPT-3.5-turbo (optional)

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/kavya5c0/MediPredict/issues
- Email: [Your Email]

---

**Last Updated:** October 11, 2026
**Status:** Development Complete - ML Models Integrated and Ready for Testing
