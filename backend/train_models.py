"""
ML Model Training Script
Trains machine learning models for disease prediction using public datasets
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create models directory
os.makedirs('models', exist_ok=True)

def train_diabetes_model():
    """Train diabetes prediction model using Pima Indians Diabetes dataset"""
    logger.info("Training Diabetes Prediction Model...")
    
    # Load Pima Indians Diabetes dataset from UCI ML Repository
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    
    try:
        df = pd.read_csv(url, names=column_names)
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        logger.info("Using synthetic data for diabetes model...")
        # Create synthetic data if download fails
        np.random.seed(42)
        n_samples = 768
        df = pd.DataFrame({
            'Pregnancies': np.random.randint(0, 18, n_samples),
            'Glucose': np.random.randint(50, 200, n_samples),
            'BloodPressure': np.random.randint(40, 120, n_samples),
            'SkinThickness': np.random.randint(0, 50, n_samples),
            'Insulin': np.random.randint(0, 600, n_samples),
            'BMI': np.random.uniform(15, 50, n_samples),
            'DiabetesPedigreeFunction': np.random.uniform(0.05, 2.5, n_samples),
            'Age': np.random.randint(21, 80, n_samples),
            'Outcome': np.random.choice([0, 1], n_samples, p=[0.67, 0.33])
        })
    
    # Features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Diabetes Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler (exclude Outcome from features)
    feature_names = [col for col in column_names if col != 'Outcome']
    joblib.dump(model, 'models/diabetes_model.pkl')
    joblib.dump(scaler, 'models/diabetes_scaler.pkl')
    joblib.dump(feature_names, 'models/diabetes_features.pkl')
    
    logger.info("Diabetes model saved successfully")
    return accuracy

def train_heart_disease_model():
    """Train heart disease prediction model using Cleveland Heart Disease dataset"""
    logger.info("Training Heart Disease Prediction Model...")
    
    # Load Cleveland Heart Disease dataset
    url = "https://raw.githubusercontent.com/plotly/datasets/master/heart.csv"
    
    try:
        df = pd.read_csv(url)
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        logger.info("Using synthetic data for heart disease model...")
        # Create synthetic data
        np.random.seed(42)
        n_samples = 303
        df = pd.DataFrame({
            'age': np.random.randint(29, 78, n_samples),
            'sex': np.random.choice([0, 1], n_samples),
            'cp': np.random.randint(0, 4, n_samples),
            'trestbps': np.random.randint(90, 200, n_samples),
            'chol': np.random.randint(120, 570, n_samples),
            'fbs': np.random.choice([0, 1], n_samples),
            'restecg': np.random.randint(0, 3, n_samples),
            'thalach': np.random.randint(80, 210, n_samples),
            'exang': np.random.choice([0, 1], n_samples),
            'oldpeak': np.random.uniform(0, 7, n_samples),
            'slope': np.random.randint(0, 3, n_samples),
            'ca': np.random.randint(0, 5, n_samples),
            'thal': np.random.randint(0, 4, n_samples),
            'target': np.random.choice([0, 1], n_samples, p=[0.54, 0.46])
        })
    
    # Features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Heart Disease Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/heart_disease_model.pkl')
    joblib.dump(scaler, 'models/heart_disease_scaler.pkl')
    joblib.dump(list(X.columns), 'models/heart_disease_features.pkl')
    
    logger.info("Heart disease model saved successfully")
    return accuracy

def train_hypertension_model():
    """Train hypertension risk prediction model"""
    logger.info("Training Hypertension Risk Model...")
    
    # Create synthetic dataset for hypertension
    np.random.seed(42)
    n_samples = 500
    df = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'bmi': np.random.uniform(15, 45, n_samples),
        'systolic_bp': np.random.randint(90, 200, n_samples),
        'diastolic_bp': np.random.randint(60, 130, n_samples),
        'cholesterol': np.random.randint(120, 350, n_samples),
        'physical_activity': np.random.randint(0, 300, n_samples),
        'smoking': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'family_history': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'hypertension_risk': np.random.choice([0, 1], n_samples, p=[0.6, 0.4])
    })
    
    # Features and target
    X = df.drop('hypertension_risk', axis=1)
    y = df['hypertension_risk']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Logistic Regression
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Hypertension Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/hypertension_model.pkl')
    joblib.dump(scaler, 'models/hypertension_scaler.pkl')
    joblib.dump(list(X.columns), 'models/hypertension_features.pkl')
    
    logger.info("Hypertension model saved successfully")
    return accuracy

def main():
    """Train all ML models"""
    logger.info("=" * 50)
    logger.info("ML Model Training Started")
    logger.info("=" * 50)
    
    try:
        diabetes_acc = train_diabetes_model()
        heart_acc = train_heart_disease_model()
        hypertension_acc = train_hypertension_model()
        
        logger.info("=" * 50)
        logger.info("ML Model Training Completed")
        logger.info("=" * 50)
        logger.info(f"Diabetes Model Accuracy: {diabetes_acc:.4f}")
        logger.info(f"Heart Disease Model Accuracy: {heart_acc:.4f}")
        logger.info(f"Hypertension Model Accuracy: {hypertension_acc:.4f}")
        logger.info("All models saved to 'models/' directory")
        
    except Exception as e:
        logger.error(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    main()
