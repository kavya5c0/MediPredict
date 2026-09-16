# Quick Start Guide - MediPredict (After API Fixes)

## ✅ What Was Fixed

All 4 critical API endpoints have been fixed to handle MongoDB connection failures gracefully:

1. **`/api/recommendations`** - Now returns general recommendations instead of 500 error
2. **`/api/predict/history`** - Now returns empty array instead of 404 error  
3. **`/api/chat/history`** - Now returns empty array instead of 404/500 error
4. **`/api/medical/upload`** - Now has better error handling and file validation

## 🚀 How to Start the Application

### Option 1: With MongoDB (Full Functionality)

#### Step 1: Start MongoDB
```bash
# Open a terminal and run:
mongod
```

#### Step 2: Start Backend
```bash
# Open a new terminal
cd C:\Users\girig\Desktop\MajorProject\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 3: Start Frontend
```bash
# Open another new terminal
cd C:\Users\girig\Desktop\MajorProject\frontend
npm run dev
```

#### Step 4: Access the Application
Open your browser and go to: `http://localhost:5173`

---

### Option 2: Without MongoDB (Limited Functionality)

The application now works even without MongoDB! Some features will use fallback data.

#### Step 1: Start Backend (Skip MongoDB)
```bash
cd C:\Users\girig\Desktop\MajorProject\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 2: Start Frontend
```bash
cd C:\Users\girig\Desktop\MajorProject\frontend
npm run dev
```

#### Step 3: Access the Application
Open your browser and go to: `http://localhost:5173`

**What works without MongoDB:**
- ✅ Disease prediction
- ✅ Health chat (with fallback responses)
- ✅ General recommendations
- ✅ UI and navigation

**What requires MongoDB:**
- ❌ User registration/login
- ❌ Saving prediction history
- ❌ Saving chat history
- ❌ Uploading medical reports
- ❌ Personalized recommendations

---

## 🧪 Testing the Fixes

### Test 1: Recommendations (Without MongoDB)
1. Start backend without MongoDB
2. Use Postman or browser to visit: `http://localhost:8000/api/recommendations`
3. **Expected**: 200 response with general recommendations (not 500 error)

### Test 2: Prediction History (Without MongoDB)
1. Visit: `http://localhost:8000/api/predict/history`
2. **Expected**: `{"predictions": []}` (not 404 error)

### Test 3: Chat History (Without MongoDB)
1. Visit: `http://localhost:8000/api/chat/history`
2. **Expected**: `{"history": []}` (not 404/500 error)

### Test 4: Medical Upload (Without MongoDB)
1. Try to upload a file
2. **Expected**: 503 error with message "Database not available. Please ensure MongoDB is running."

---

## 📝 Common Issues & Solutions

### Issue: "uvicorn: command not found"
**Solution**: Install uvicorn
```bash
pip install uvicorn
```

### Issue: "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Issue: "Port 8000 already in use"
**Solution**: Kill the process or use a different port
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```
Then update frontend `.env` file to use `VITE_API_URL=http://localhost:8001`

### Issue: "MongoDB connection failed"
**Solution**: Either:
1. Start MongoDB with `mongod`, OR
2. Continue without MongoDB (limited functionality)

---

## 📊 API Status After Fixes

| Endpoint | Status | With MongoDB | Without MongoDB |
|----------|--------|--------------|-----------------|
| `/api/recommendations` | ✅ Fixed | Personalized | General |
| `/api/predict/history` | ✅ Fixed | Full history | Empty array |
| `/api/chat/history` | ✅ Fixed | Full history | Empty array |
| `/api/medical/upload` | ✅ Fixed | Saves to DB | Returns 503 |
| `/api/predict/disease` | ✅ Works | Saves history | No save |
| `/api/chat/query` | ✅ Works | Saves history | No save |

---

## 🎯 Next Steps

1. **Test the application** - Try the fixed endpoints
2. **Install MongoDB** - For full functionality
3. **Review the logs** - Check for any remaining issues
4. **Report any bugs** - If you find issues, report them with details

---

## 📄 Related Documentation

- `API_ERROR_FIXES.md` - Detailed technical documentation of all fixes
- `README.md` - Full project documentation
- `SETUP_GUIDE.md` - Complete setup instructions

---

## ✨ Summary

**Before Fixes**: Application crashed with 500/404 errors when MongoDB was down  
**After Fixes**: Application works gracefully with fallback responses

All critical API errors have been resolved! 🎉
