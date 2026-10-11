# MediPredict - Complete Setup & Testing Guide

## 📋 Table of Contents
1. [PostgreSQL Setup](#postgresql-setup)
2. [Application Configuration](#application-configuration)
3. [Running the Application](#running-the-application)
4. [Testing Each Feature](#testing-each-feature)
5. [Chatbot Explanation](#chatbot-explanation)
6. [Viewing Data in pgAdmin](#viewing-data-in-pgadmin)

---

## 🗄️ PostgreSQL Setup

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

## ⚙️ Application Configuration

### **Step 1: Configure Backend Environment**

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

### **Step 3: Install Frontend Dependencies**

```bash
cd C:\Users\girig\Desktop\MajorProject\frontend
npm install
```

---

## 🚀 Running the Application

### **Step 1: Start Backend**

Open a terminal and run:
```bash
cd C:\Users\girig\Desktop\MajorProject\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: PostgreSQL connection pool created successfully
INFO: RAG system initialized with OpenAI API
INFO: Application startup complete
```

### **Step 2: Start Frontend**

Open a NEW terminal and run:
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

## 🧪 Testing Each Feature

### **1. User Registration**

**Why Built:** To authenticate users and save their health data securely.

**How to Test:**
1. Go to **Register** page
2. Fill in:
   - Full Name: Test User
   - Email: test@example.com
   - Password: password123
   - Age: 25
   - Gender: Female
3. Click **"Sign Up"**

**Expected Result:**
- Success message
- Redirect to login page
- User saved to PostgreSQL

**Verify in pgAdmin:**
- Right-click `users` table → View/Edit Data → All Rows
- See your registered user

---

### **2. User Login**

**Why Built:** To authenticate users with JWT tokens for secure session management.

**How to Test:**
1. Go to **Login** page
2. Enter email and password from registration
3. Click **"Login"**

**Expected Result:**
- Success message
- Redirect to Dashboard
- JWT token stored in localStorage

---

### **3. Disease Prediction**

**Why Built:** To calculate disease risk based on health parameters using evidence-based medical criteria.

**How to Test:**
1. Go to **Disease Prediction** page
2. Fill in health data:
   - Age: 25
   - BMI: 28
   - Blood Pressure: 130/85
   - Glucose: 110 mg/dL
   - Physical Activity: 120 min/week
   - Smoking: No
3. Click **"Get Prediction"**

**Expected Result:**
- Risk assessment for diabetes
- Risk assessment for cardiovascular disease
- Personalized recommendations
- Results saved to PostgreSQL

**Verify in pgAdmin:**
- Right-click `predictions` table → View/Edit Data → All Rows
- See your prediction results

---

### **4. Medical Report Analysis**

**Why Built:** To analyze medical reports, extract lab values, and provide clinical interpretation using ICD-10 codes.

**How to Test:**
1. Go to **Medical Reports** page
2. Enter medical text (or upload file):
   ```
   Glucose: 145 mg/dL
   Blood Pressure: 142/92 mmHg
   Cholesterol: 220 mg/dL
   ```
3. Click **"Analyze Text"**

**Expected Result:**
- Extracted lab values
- Clinical significance
- ICD-10 code suggestions
- Medical terminology interpretation
- Analysis saved to PostgreSQL

**Verify in pgAdmin:**
- Right-click `medical_reports` table → View/Edit Data → All Rows
- See your report analysis

---

### **5. Health Chatbot**

**Why Built:** To provide AI-powered medical information and health guidance.

**How to Test:**
1. Go to **Health Chat** page
2. Ask health questions:
   - "I have high fever"
   - "Why do I get back pain?"
   - "What are diabetes symptoms?"
   - "How can I reduce blood pressure?"
3. See the response

**Expected Result:**
- Specific medical information (not generic)
- Evidence-based guidance
- Medical disclaimer
- Chat history saved to PostgreSQL

**What the Chatbot Uses:**
- **Medical Knowledge Base**: Real data from WHO, CDC, Mayo Clinic, NIH, AHA
- **Keyword Matching**: Searches for relevant medical information
- **Specific Information**: Fever, back pain, diabetes, hypertension, heart disease

**Why OpenAI API Key Not Available:**
- OpenAI no longer provides free credits to new accounts
- Requires manual credit addition ($5-10 minimum)
- Without credits, uses our comprehensive medical knowledge base
- With credits, would use GPT-3.5-turbo for dynamic AI responses

**Current Behavior:**
- ✅ Provides specific medical information (fever causes, when to see doctor, home care)
- ✅ Uses real medical data from reputable sources
- ✅ Evidence-based and medically accurate
- ❌ Not dynamic AI-generated (requires OpenAI credits)

**Verify in pgAdmin:**
- Right-click `chat_history` table → View/Edit Data → All Rows
- See your chat conversations

---

### **6. Health Recommendations**

**Why Built:** To provide age-appropriate screening guidelines and personalized health recommendations.

**How to Test:**
1. Go to **Recommendations** page
2. View recommendations based on your age

**Expected Result:**
- Age-based screening guidelines (USPSTF)
- Lifestyle recommendations (diet, exercise, sleep)
- Preventive health measures
- Personalized based on health profile

**Age-Based Examples:**
- **18-39**: Blood pressure, cholesterol, BMI checks
- **40-49**: Mammograms, colon cancer screening
- **50-64**: Bone density, lung cancer screening
- **65+**: Comprehensive screening, vaccines

---

### **7. Dashboard**

**Why Built:** To visualize health data, trends, and predictions in an intuitive interface.

**How to Test:**
1. Go to **Dashboard** page
2. View charts and health metrics

**Expected Result:**
- Health overview with key metrics
- Disease risk visualization
- Health trends (if multiple predictions)
- Interactive Highcharts

---

## 🤖 Chatbot Explanation

### **What the Chatbot Does:**

The chatbot provides medical information and health guidance using:

1. **Medical Knowledge Base**
   - Real data from WHO, CDC, Mayo Clinic, NIH, American Heart Association
   - Evidence-based medical information
   - Clinical practice guidelines

2. **Keyword Matching System**
   - Searches for relevant medical terms in your question
   - Matches against our knowledge base
   - Returns specific, targeted information

3. **Specific Medical Information**
   - **Fever**: Causes, when to see doctor, home care, temperature ranges
   - **Back Pain**: Causes, prevention, when to see doctor
   - **Diabetes**: Symptoms, risk factors, prevention
   - **Hypertension**: Symptoms, target BP, prevention
   - **Heart Disease**: Symptoms, risk factors, prevention

### **Why OpenAI API Key is Not Available:**

**The Problem:**
- OpenAI changed their policy
- New accounts no longer get automatic free credits
- Must add payment method and credits manually ($5-10 minimum)
- Without credits, API returns "429 - No credits remaining" error

**Current Solution:**
- Uses our comprehensive medical knowledge base
- Provides specific, evidence-based information
- Medically accurate and reliable
- No cost to use

**Future Enhancement (with OpenAI credits):**
- Would use GPT-3.5-turbo for dynamic AI responses
- Each response would be unique and contextual
- More conversational and personalized
- Still based on our medical knowledge base for accuracy

### **Chatbot Technology Stack:**

**Current (Without OpenAI):**
- Medical Knowledge Base (static, evidence-based)
- Keyword Matching (smart search)
- Specific Medical Information (fever, back pain, diabetes, etc.)
- No API cost

**Future (With OpenAI credits):**
- Medical Knowledge Base (retrieval)
- OpenAI GPT-3.5-turbo (generation)
- Dynamic AI responses (unique per question)
- Minimal API cost (~$0.001-0.005 per response)

---

## 📊 Viewing Data in pgAdmin

### **Step 1: Open pgAdmin 4**
- From Start menu, open pgAdmin 4
- Connect to PostgreSQL server with your password

### **Step 2: View User Data**
1. Expand **Servers** → **PostgreSQL 16** → **Databases** → **healthcare_db**
2. Expand **Schemas** → **public** → **Tables**
3. Right-click on `users` table
4. Click **"View/Edit Data"** → **"All Rows"**
5. See all registered users with their information

### **Step 3: View Chat History**
1. Right-click on `chat_history` table
2. Click **"View/Edit Data"** → **"All Rows"**
3. See all chat conversations with questions and answers

### **Step 4: View Predictions**
1. Right-click on `predictions` table
2. Click **"View/Edit Data"** → **"All Rows"**
3. See all disease predictions with risk assessments

### **Step 5: View Medical Reports**
1. Right-click on `medical_reports` table
2. Click **"View/Edit Data"** → **"All Rows"**
3. See all analyzed medical reports

---

## 🔍 Troubleshooting

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

### **Frontend Won't Start**

**Error:** Port already in use

**Solution:**
- Frontend will automatically try ports 3000-3005
- Check which port it starts on
- Access that URL (e.g., http://localhost:3005)

### **Registration 500 Error**

**Error:** Internal Server Error during registration

**Solution:**
1. Check backend logs for specific error
2. Verify PostgreSQL is running
3. Verify database `healthcare_db` exists
4. Check password in `.env`

---

## 📚 Data Sources

All medical information is from reputable sources:

- **World Health Organization (WHO)** - Global health guidelines
- **Centers for Disease Control and Prevention (CDC)** - Public health data
- **Mayo Clinic** - Clinical practice guidelines
- **National Institutes of Health (NIH)** - Medical research
- **American Heart Association (AHA)** - Cardiovascular guidelines
- **US Preventive Services Task Force (USPSTF)** - Screening recommendations

---

## 🎯 Application Summary

### **Features Working:**
- ✅ User Authentication (JWT-based)
- ✅ Disease Prediction (evidence-based)
- ✅ Medical Report Analysis (ICD-10 codes)
- ✅ Health Chatbot (specific medical information)
- ✅ Health Recommendations (age-based)
- ✅ Dashboard (data visualization)
- ✅ PostgreSQL Persistence (real database)

### **Technology Stack:**
- **Backend**: FastAPI, Uvicorn, PostgreSQL
- **Frontend**: React, Vite, Highcharts
- **Database**: PostgreSQL
- **AI/ML**: Medical knowledge base (evidence-based)

### **Current Limitations:**
- ⚠️ Chatbot uses static medical knowledge (requires OpenAI credits for dynamic AI)
- ⚠️ No real OCR for medical images
- ⚠️ Disease prediction uses rule-based, not ML models

---

## 🚀 Next Steps

1. **Test all features** using this guide
2. **View data in pgAdmin** to verify database persistence
3. **Add OpenAI credits** (optional) for dynamic chatbot responses
4. **Deploy to Render** (optional) for public access

---

**Last Updated:** October 11, 2026
**Status:** Fully Functional with PostgreSQL and Real Medical Data
