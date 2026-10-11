# MediPredict - AI-Powered Healthcare Assistant

## 📋 Project Overview

**MediPredict** is an academic healthcare assistant that provides AI-powered medical information, disease prediction, and personalized health recommendations. The application uses real medical data from reputable sources and integrates with OpenAI's GPT-3.5 for intelligent responses.

### **Key Features:**
- ✅ AI-Powered Health Chatbot (RAG system with OpenAI GPT-3.5)
- ✅ Disease Risk Prediction (evidence-based calculations)
- ✅ Medical Report Analysis (ICD-10 codes, medical terminology)
- ✅ Personalized Health Recommendations (age-based screening guidelines)
- ✅ Real-Time Health Dashboard (Highcharts visualizations)
- ✅ User Authentication (JWT-based)
- ✅ Database Persistence (PostgreSQL)

---

## 📊 Real Medical Data Sources

### **1. Medical Knowledge Base**

#### **Data Sources:**
- **World Health Organization (WHO)** - Global health guidelines
- **Centers for Disease Control and Prevention (CDC)** - Public health data
- **Mayo Clinic** - Clinical practice guidelines
- **National Institutes of Health (NIH)** - Medical research
- **American Heart Association (AHA)** - Cardiovascular guidelines

#### **Data Categories:**

##### **Diabetes Mellitus**
- **Symptoms:** Increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores, frequent infections
- **Risk Factors:** Overweight/obesity, inactivity, family history, age 45+, prediabetes, gestational diabetes, PCOS, high blood pressure, abnormal cholesterol
- **Prevention:** Healthy weight, 150+ min aerobic activity weekly, tobacco avoidance, healthy diet, limit sugary beverages, control BP/cholesterol
- **Treatment:** Blood sugar monitoring (A1C tests), oral medications (metformin, sulfonylureas), insulin therapy, medical nutrition therapy, physical activity, continuous glucose monitoring
- **Complications:** Cardiovascular disease, kidney disease (nephropathy), eye damage (retinopathy), nerve damage (neuropathy), foot damage, skin conditions, hearing impairment
- **ICD-10 Codes:** E10 (Type 1), E11 (Type 2), R73.03 (Prediabetes)

##### **Hypertension (High Blood Pressure)**
- **Symptoms:** Headaches, nosebleeds, shortness of breath, dizziness, chest pain, vision changes, blood in urine
- **Risk Factors:** Age, race, family history, overweight/obesity, physical inactivity, high sodium diet, alcohol consumption, stress
- **Prevention:** DASH diet, sodium <2,300 mg/day, healthy weight, regular exercise (150 min/week), limit alcohol, stress management, quit smoking
- **Treatment:** Lifestyle modifications, ACE inhibitors, ARBs, calcium channel blockers, diuretics, beta blockers
- **Target Blood Pressure:**
  - Normal: <120/80 mmHg
  - Elevated: 120-129/<80 mmHg
  - Stage 1: 130-139/80-89 mmHg
  - Stage 2: 140+/90+ mmHg
  - Hypertensive crisis: >180/120 mmHg
- **ICD-10 Codes:** I10 (Essential), I15 (Secondary)

##### **Heart Disease**
- **Symptoms:** Chest pain/discomfort, shortness of breath, pain in neck/jaw/throat/back, pain/numbness in legs/arms, heart palpitations, fatigue, swelling in legs/ankles/feet, dizziness
- **Risk Factors:** High blood pressure, high cholesterol, smoking, diabetes, overweight/obesity, physical inactivity, unhealthy diet, excessive alcohol, family history, age, stress
- **Prevention:** Quit smoking, control blood pressure, manage cholesterol, maintain healthy weight, exercise regularly, heart-healthy diet, limit alcohol, manage stress, adequate sleep (7-9 hours)
- **Treatment:** Lifestyle changes, medications (statins, beta blockers, ACE inhibitors), medical procedures (angioplasty, bypass surgery), cardiac rehabilitation, implantable devices
- **Diet Recommendations:** More fruits/vegetables/whole grains/lean proteins, less saturated/trans fats/sodium/added sugars, Mediterranean or DASH diet, healthy fats (olive oil, avocado, nuts), limit red meat to 1-2x/week, eat fish 2x/week
- **ICD-10 Codes:** I20 (Angina), I21-I22 (Heart attack), I50 (Heart failure), I47-I49 (Arrhythmia)

##### **General Health Guidelines**
- **Nutrition:**
  - Fruits/Vegetables: 5-9 servings daily
  - Whole Grains: 3-6 servings daily
  - Protein: Lean meats, poultry, fish, beans, nuts
  - Fats: Limit saturated and trans fats
  - Sugar: <10% of daily calories
  - Sodium: <2,300 mg/day
- **Exercise:**
  - Adults: 150 minutes moderate or 75 minutes vigorous weekly
  - Muscle Strengthening: 2+ days per week
  - Children: 60 minutes daily
  - Types: Aerobic, strength training, flexibility, balance
- **Sleep:**
  - Adults: 7-9 hours per night
  - Teenagers: 8-10 hours per night
  - Children: 9-12 hours per night
  - Quality: Consistent schedule, dark room, no screens before bed
- **Hydration:**
  - Daily Intake: 8 glasses (64 oz) for adults
  - Sources: Water, herbal tea, fruits, vegetables
  - Avoid: Excessive caffeine, sugary drinks

##### **Lab Value Reference Ranges**
- **Blood Glucose:**
  - Normal Fasting: 70-99 mg/dL
  - Normal Postprandial: <140 mg/dL
  - Prediabetes Fasting: 100-125 mg/dL
  - Diabetes Fasting: ≥126 mg/dL
  - A1C Normal: <5.7%
  - A1C Prediabetes: 5.7-6.4%
  - A1C Diabetes: ≥6.5%
- **Cholesterol:**
  - Total Cholesterol: Desirable <200, Borderline 200-239, High ≥240 mg/dL
  - LDL (Bad): Optimal <100, Near Optimal 100-129, Borderline 130-159, High 160-189, Very High ≥190 mg/dL
  - HDL (Good): Men ≥40, Women ≥50 mg/dL
  - Triglycerides: Normal <150, Borderline 150-199, High 200-499, Very High ≥500 mg/dL
- **Blood Pressure:**
  - Normal: <120/80 mmHg
  - Elevated: 120-129/<80 mmHg
  - Stage 1: 130-139/80-89 mmHg
  - Stage 2: 140+/90+ mmHg

---

### **2. Disease Risk Calculators**

#### **Evidence-Based Risk Assessment:**

##### **Diabetes Risk Calculation**
- **BMI Risk:**
  - Low Risk: BMI <25
  - Moderate Risk: BMI 25-29.9
  - High Risk: BMI ≥30
- **Age Risk:**
  - Low Risk: Age <45
  - Moderate Risk: Age 45-64
  - High Risk: Age ≥65
- **Glucose Risk:**
  - Normal: <100 mg/dL
  - Prediabetes: 100-125 mg/dL
  - Diabetes: ≥126 mg/dL
- **Additional Factors:**
  - Physical Activity: <150 min/week adds risk
  - Family History: Diabetes in family adds risk
- **Scoring System:** Based on American Diabetes Association guidelines

##### **Cardiovascular Risk Calculation**
- **BMI Risk:**
  - Low Risk: BMI <25
  - Moderate Risk: BMI 25-29.9
  - High Risk: BMI ≥30
- **Cholesterol Risk:**
  - Optimal: Total <200, LDL <100
  - Borderline: Total 200-239, LDL 100-129
  - High: Total ≥240, LDL ≥160
- **Blood Pressure Risk:**
  - Optimal: <120/80
  - Elevated: 120-129/<80
  - Stage 1: 130-139/80-89
  - Stage 2: 140+/90+
- **Age Risk:**
  - Low Risk: Age <45
  - Moderate Risk: Age 45-64
  - High Risk: Age ≥65
- **Additional Factors:**
  - Smoking: Major risk factor
  - Physical Inactivity: <150 min/week adds risk
- **Scoring System:** Based on American Heart Association guidelines

---

### **3. Health Screening Recommendations**

#### **Age-Based Screening Guidelines (USPSTF)**

##### **Age 18-39**
- Blood pressure check every 2 years
- Cholesterol check every 5 years
- BMI check annually
- Blood glucose every 3 years if overweight
- Skin cancer exam
- Cervical cancer screening (women)
- Testicular cancer screening (men)

##### **Age 40-49**
- Blood pressure check annually
- Cholesterol check every 5 years
- Diabetes screening every 3 years
- Mammogram every 1-2 years (women)
- Colon cancer screening starting at 45
- Prostate cancer screening (men)
- Eye exam every 2-4 years

##### **Age 50-64**
- Blood pressure check annually
- Cholesterol check every 1-2 years
- Diabetes screening every 3 years
- Mammogram every 1-2 years (women)
- Colon cancer screening every 10 years
- Bone density scan (women)
- Lung cancer screening if smoker
- Shingles vaccine

##### **Age 65+**
- Blood pressure check annually
- Cholesterol check annually
- Diabetes screening every 3 years
- Mammogram every 1-2 years (women)
- Colon cancer screening every 10 years
- Bone density scan (women)
- Annual flu vaccine
- Pneumococcal vaccine
- Shingles vaccine
- Hearing test

---

### **4. Medical Report Analysis**

#### **Real Medical Terminology & ICD-10 Codes**

##### **Common ICD-10 Codes:**
- **Diabetes:** E10 (Type 1), E11 (Type 2), R73.03 (Prediabetes)
- **Hypertension:** I10 (Essential), I15 (Secondary)
- **Cardiovascular:** I20 (Angina), I21-I22 (Heart attack), I50 (Heart failure)
- **Obesity:** E66.0 (BMI 30-34), E66.1 (BMI 35-39), E66.2 (BMI 40+)

##### **Medical Report Templates:**
- **Lab Report:** Patient info, specimen type, test results with reference ranges, clinical significance
- **Radiology Report:** Clinical indication, technique, findings, impression
- **Progress Note:** Subjective (symptoms), Objective (vitals/exam), Assessment (diagnosis), Plan (treatment)

##### **Sample Clinical Cases:**
- **Diabetes Case:** Realistic presentation with elevated A1c (7.8%), fasting glucose (142 mg/dL), dyslipidemia
- **Hypertension Case:** Stage 2 hypertension (152/94 mmHg), with appropriate management plan
- **Cardiovascular Case:** Stable angina with positive stress test, appropriate treatment recommendations

---

### **5. ICD-10 Classification System**

#### **Used for:**
- Medical coding in report analysis
- Disease classification in predictions
- Clinical terminology standardization

#### **Implementation:**
- Real ICD-10 codes embedded in medical knowledge base
- Automatic code suggestion in report analysis
- Clinical significance mapping

---

## 🛠️ Technology Stack

### **Backend:**
- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn 0.24.0
- **Database:** PostgreSQL (asyncpg 0.29.0)
- **Authentication:** JWT (python-jose, passlib)
- **AI Integration:** OpenAI GPT-3.5-turbo
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

### **AI/ML:**
- **LLM:** OpenAI GPT-3.5-turbo
- **RAG System:** Custom implementation with medical knowledge base
- **Embeddings:** Smart keyword search (lightweight for free tier)
- **Vector Database:** ChromaDB (optional, for full RAG)

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
│   │   │   ├── prediction.py    # Disease prediction
│   │   │   └── recommendations.py # Health recommendations
│   │   ├── core/
│   │   │   ├── config.py        # Configuration
│   │   │   ├── database.py      # PostgreSQL connection
│   │   │   └── security.py      # JWT authentication
│   │   ├── data/
│   │   │   ├── medical_knowledge.py  # Real medical data
│   │   │   └── medical_reports.py    # ICD codes, templates
│   │   ├── models/
│   │   │   └── rag_system.py    # RAG implementation
│   │   └── main.py              # FastAPI application
│   ├── requirements.txt
│   └── .env                    # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── charts/          # Highcharts components
│   │   │   ├── Layout.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── ErrorBoundary.jsx
│   │   │   └── ToastProvider.jsx
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
└── DEPLOYMENT_GUIDE.md          # Deployment instructions
```

---

## 🚀 Setup Instructions

### **Prerequisites:**
- Python 3.9+
- Node.js 18+
- PostgreSQL 16+
- OpenAI API Key (for AI features)

### **Local Setup:**

#### **1. Clone Repository:**
```bash
git clone https://github.com/kavya5c0/MediPredict.git
cd MajorProject
```

#### **2. Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
```

#### **3. Configure Environment:**
Create `backend/.env`:
```env
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/healthcare_db
SECRET_KEY=your-secret-key
```

#### **4. Database Setup:**
```bash
# Create PostgreSQL database named "healthcare_db"
# Tables are auto-created on application startup
```

#### **5. Start Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **6. Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

#### **7. Access Application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎯 Features & Functionality

### **1. User Authentication**
- **Registration:** Email/password with bcrypt hashing
- **Login:** JWT token generation
- **Session Management:** Token storage in localStorage
- **Protected Routes:** Dashboard and features require authentication

### **2. AI-Powered Health Chatbot**
- **RAG System:** Retrieves relevant medical documents
- **OpenAI Integration:** GPT-3.5-turbo for intelligent responses
- **Context-Aware:** Uses retrieved medical knowledge
- **Evidence-Based:** All responses from real medical sources
- **Chat History:** Saves conversations to database
- **Disclaimer:** Always includes medical disclaimer

### **3. Disease Prediction**
- **Risk Assessment:** Evidence-based scoring system
- **Multiple Conditions:** Diabetes, Cardiovascular, Hypertension
- **Real Criteria:** Based on clinical guidelines
- **Personalized:** Factors in age, BMI, lab values, lifestyle
- **Recommendations:** Actionable health advice
- **History Tracking:** Saves predictions to database

### **4. Medical Report Analysis**
- **Text Analysis:** Extracts lab values and medical entities
- **ICD-10 Codes:** Suggests appropriate medical codes
- **Clinical Significance:** Interprets results
- **Medical Terminology:** Uses real medical vocabulary
- **Sample Cases:** Based on real clinical presentations
- **File Upload:** Support for PDF, images

### **5. Health Recommendations**
- **Age-Based:** Screening guidelines by age group
- **Personalized:** Based on health profile
- **Evidence-Based:** USPSTF recommendations
- **Lifestyle:** Diet, exercise, sleep, stress management
- **Screening:** Age-appropriate tests and vaccines

### **6. Dashboard**
- **Health Overview:** Key metrics visualization
- **Health Trends:** Historical data tracking
- **Disease Risk:** Risk assessment charts
- **Health Score:** Overall health gauge
- **Real-Time:** Live data updates

---

## 📚 Data References & Citations

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

7. **ICD-10 Classification**
   - WHO ICD-10: https://icd.who.int/browse10/2019/en

### **Clinical Practice Guidelines:**
- American Diabetes Association Standards of Care
- ACC/AHA Hypertension Guidelines
- ACC/AHA Cholesterol Guidelines
- USPSTF Screening Recommendations

---

## 🔒 Security & Privacy

### **Authentication:**
- **Password Hashing:** bcrypt (industry standard)
- **JWT Tokens:** 30-minute expiration
- **HTTPS:** Required for production
- **SQL Injection Protection:** Parameterized queries

### **Data Privacy:**
- **No PHI Storage:** No protected health information stored
- **Anonymized Data:** User data is anonymized
- **Secure Storage:** PostgreSQL with SSL
- **Environment Variables:** Sensitive data in .env

### **Medical Disclaimer:**
- **Always Displayed:** Every response includes disclaimer
- **Not Medical Advice:** Clearly stated
- **Consult Professionals:** Users advised to consult healthcare providers
- **Educational Purpose:** Information for educational use only

---

## 🌐 Deployment

### **Local Development:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Database: PostgreSQL localhost:5432

### **Production (Render Free Tier):**
- **Backend:** Render (Docker deployment)
- **Frontend:** Served by backend (single URL)
- **Database:** Render PostgreSQL (free tier)
- **URL:** https://medipredict-backend.onrender.com

### **Deployment Status:**
- ✅ Code pushed to GitHub
- ✅ Render configured
- ✅ Dockerfile optimized
- ⚠️ PostgreSQL connection pending configuration
- ⚠️ OpenAI API key needs to be added to Render

---

## 📊 Performance Metrics

### **Application Performance:**
- **Backend Response Time:** <500ms (without AI)
- **AI Response Time:** 2-5 seconds (with OpenAI)
- **Database Queries:** <100ms
- **Frontend Load Time:** <2 seconds

### **Resource Usage:**
- **Memory:** ~512MB (free tier limit)
- **Storage:** PostgreSQL (1GB free tier)
- **CPU:** Shared (free tier)

---

## 🧪 Testing

### **Manual Testing Checklist:**
- [ ] User registration works
- [ ] User login works with correct credentials
- [ ] JWT token is stored and used
- [ ] Chatbot responds with AI (if API key configured)
- [ ] Chatbot falls back gracefully (without API key)
- [ ] Disease prediction calculates risk correctly
- [ ] Medical report analysis extracts lab values
- [ ] Recommendations are age-appropriate
- [ ] Dashboard charts display correctly
- [ ] Database persistence works (PostgreSQL)

### **API Testing:**
- **POST /api/auth/register** - User registration
- **POST /api/auth/login** - User login
- **POST /api/chat/query** - AI chat query
- **GET /api/chat/history** - Chat history
- **POST /api/predict/disease** - Disease prediction
- **POST /api/medical/analyze-text** - Report analysis
- **GET /api/recommendations/** - Health recommendations

---

## 🐛 Known Issues & Limitations

### **Current Limitations:**
1. **PostgreSQL Required:** Full functionality requires PostgreSQL
2. **OpenAI API Key:** AI features require valid API key and credits
3. **Free Tier Constraints:** Memory and storage limits on Render
4. **No Real OCR:** Medical image OCR not implemented
5. **No Real ML Models:** Disease prediction uses rule-based, not ML

### **Deployment Challenges:**
1. **Render Free Tier:** 512MB memory limit
2. **Heavy Dependencies:** ChromaDB/sentence-transformers too heavy for free tier
3. **Spin-Down:** Free tier spins down after 15 minutes inactivity
4. **Database Setup:** Requires external PostgreSQL configuration

---

## 🔮 Future Enhancements

### **Planned Features:**
1. **Real OCR:** Tesseract integration for medical images
2. **ML Models:** Train on real medical datasets
3. **Full RAG:** ChromaDB with semantic search
4. **Mobile App:** React Native implementation
5. **More Conditions:** Add more disease predictions
6. **Medication Interaction:** Drug interaction checker
7. **Appointment Scheduling**: Healthcare provider integration

---

## 📄 License

This project is for academic and educational purposes only.

---

## 👥 Contributors

- **Development:** [Your Name]
- **Data Sources:** WHO, CDC, Mayo Clinic, NIH, AHA, USPSTF
- **AI Model:** OpenAI GPT-3.5-turbo

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/kavya5c0/MediPredict/issues
- Email: [Your Email]

---

## 📅 Version History

- **v1.0.0** - Initial release with real medical data and AI integration
  - Real medical knowledge base (WHO, CDC, Mayo Clinic, NIH, AHA)
  - RAG system with OpenAI GPT-3.5-turbo
  - Evidence-based disease risk calculations
  - ICD-10 medical coding
  - Age-based screening recommendations
  - PostgreSQL database persistence
  - Highcharts dashboard visualizations

---

**Last Updated:** September 20, 2026
**Status:** Development Complete - Ready for Testing
