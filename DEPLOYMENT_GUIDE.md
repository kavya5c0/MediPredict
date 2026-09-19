# Free Tier Deployment Guide - MediPredict

This guide will help you deploy your MediPredict healthcare application using free tiers.

## 🚀 Deployment Strategy

**Backend**: Render (Free Tier)  
**Frontend**: Vercel (Free Tier)  
**Database**: Render PostgreSQL (Free Tier) or MongoDB Atlas (Free Tier)

## 📋 Prerequisites

1. **GitHub Account** - For code hosting
2. **Render Account** - [render.com](https://render.com) (Free tier available)
3. **Vercel Account** - [vercel.com](https://vercel.com) (Free tier available)
4. **MongoDB Atlas Account** (Optional) - [mongodb.com](https://mongodb.com) (Free tier available)

## 🛠️ Step 1: Prepare Your Code

### 1.1 Update Backend Configuration

The code has been optimized for free tier deployment with these changes:

- **Lightweight dependencies**: Removed heavy PyTorch/transformers
- **Feature flags**: ML models and OCR can be disabled
- **Keyword fallback**: RAG system works without OpenAI API
- **Optimized imports**: Uses scikit-learn instead of PyTorch

### 1.2 Update Disease Prediction Model

Edit your prediction API to use the lightweight model:

```python
# In backend/app/api/prediction.py
from app.models.disease_model_lite import DiseasePredictorLite

# Replace DiseasePredictor with DiseasePredictorLite
predictor = DiseasePredictorLite()
```

### 1.3 Disable Heavy Features (Optional)

If you need to further reduce memory usage, edit `backend/app/main.py`:

```python
# Comment out heavy imports
# from app.api import medical  # OCR-heavy
# from app.api import chat    # RAG-heavy
```

## 🐳 Step 2: Deploy Backend to Render

### 2.1 Push Code to GitHub

```bash
git add .
git commit -m "Optimize for free tier deployment"
git push origin main
```

### 2.2 Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repository

### 2.3 Deploy Backend

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure deployment:
   - **Name**: `medipredict-backend`
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile`
4. Add environment variables (see `.render.env` file)
5. Click **"Deploy Web Service"**

### 2.4 Set Up Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `medipredict-db`
3. **Plan**: Free
4. Click **"Create Database"**
5. Copy the connection string to your backend environment variables

### 2.5 Optional: MongoDB Atlas

If you prefer MongoDB over PostgreSQL:

1. Go to [MongoDB Atlas](https://mongodb.com)
2. Create free cluster (M0)
3. Get connection string
4. Add to Render environment variables as `MONGODB_URI`

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Deploy Frontend

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add environment variable:
   - `VITE_API_URL`: Your Render backend URL
6. Click **"Deploy"**

### 3.2 Update API URL

After backend deployment, update frontend environment:

1. Get your backend URL from Render (e.g., `https://medipredict-backend.onrender.com`)
2. Update `frontend/.env.production`:
   ```
   VITE_API_URL=https://medipredict-backend.onrender.com
   ```
3. Redeploy frontend on Vercel

## 🔧 Step 4: Configure Environment Variables

### Required Environment Variables for Render Backend:

```bash
# Database (provided by Render)
DATABASE_URL=postgresql://...

# Optional: MongoDB Atlas
MONGODB_URI=mongodb+srv://...

# Optional: OpenAI API (uses keyword fallback if not provided)
OPENAI_API_KEY=your_key_here

# Security
SECRET_KEY=generate_with_openssl

# Feature Flags (set to false to reduce memory)
ENABLE_ML_MODELS=false
ENABLE_OCR=false
ENABLE_RAG=true
```

## 🧪 Step 5: Test Deployment

### 5.1 Test Backend

```bash
# Test health endpoint
curl https://medipredict-backend.onrender.com/health

# Test API root
curl https://medipredict-backend.onrender.com/
```

### 5.2 Test Frontend

1. Open your Vercel URL
2. Test user registration/login
3. Test basic features (without heavy ML)

## 📊 Step 6: Monitor and Optimize

### Render Free Tier Limitations:

- **512MB RAM** - May be tight for ML models
- **0.1 CPU** - Spins down after 15min inactivity
- **Cold starts** - First request may be slow (~30s)

### Optimization Tips:

1. **Keep only essential features enabled**
2. **Use PostgreSQL instead of MongoDB** (Render native)
3. **Disable OCR and heavy ML models**
4. **Implement caching** to reduce cold starts
5. **Monitor logs** in Render dashboard

## 🔄 Step 7: Update API Endpoints in Frontend

Make sure your frontend API calls use the production URL:

```javascript
// In frontend src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

## 🐛 Troubleshooting

### Common Issues:

**Issue**: Backend deployment fails
- **Solution**: Check Render logs, ensure Dockerfile is correct

**Issue**: Frontend can't connect to backend
- **Solution**: Check CORS settings in backend, verify API URL

**Issue**: Out of memory errors
- **Solution**: Disable more features, reduce model complexity

**Issue**: Slow cold starts
- **Solution**: This is normal on free tier, consider paid tier for production

## 📈 Scaling Beyond Free Tier

If you need better performance:

1. **Render Paid Tier**: $7/month for better performance
2. **Railway**: $5/month, better for ML workloads
3. **DigitalOcean**: $4-6/month VPS with full control

## 🎯 Academic Project Tips

For academic demonstration:

1. **Focus on core functionality** - authentication, basic predictions
2. **Use keyword-based RAG** - Works without OpenAI API
3. **Disable heavy features** - OCR, complex ML models
4. **Prepare demo data** - Pre-load some medical knowledge
5. **Document limitations** - Show you understand deployment constraints

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Backend deployed to Render
- [ ] Database configured (PostgreSQL/MongoDB)
- [ ] Environment variables set
- [ ] Frontend deployed to Vercel
- [ ] API URL updated in frontend
- [ ] Basic functionality tested
- [ ] Documentation updated

## 🆘 Getting Help

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **MongoDB Atlas**: [docs.mongodb.com](https://docs.mongodb.com)

---

**Note**: This deployment is optimized for academic demonstration. For production use, consider paid tiers for better performance and reliability.