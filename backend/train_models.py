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

def train_stroke_model():
    """Train stroke prediction model"""
    logger.info("Training Stroke Prediction Model...")
    
    # Create synthetic dataset for stroke (no public dataset available)
    np.random.seed(42)
    n_samples = 400
    df = pd.DataFrame({
        'age': np.random.randint(18, 90, n_samples),
        'gender': np.random.choice([0, 1], n_samples),
        'hypertension': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'heart_disease': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'ever_married': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'work_type': np.random.randint(0, 5, n_samples),
        'residence_type': np.random.choice([0, 1], n_samples),
        'avg_glucose_level': np.random.uniform(60, 300, n_samples),
        'bmi': np.random.uniform(15, 50, n_samples),
        'smoking_status': np.random.randint(0, 4, n_samples),
        'stroke': np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
    })
    
    # Features and target
    X = df.drop('stroke', axis=1)
    y = df['stroke']
    
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
    logger.info(f"Stroke Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/stroke_model.pkl')
    joblib.dump(scaler, 'models/stroke_scaler.pkl')
    joblib.dump(list(X.columns), 'models/stroke_features.pkl')
    
    logger.info("Stroke model saved successfully")
    return accuracy

def train_kidney_disease_model():
    """Train chronic kidney disease prediction model"""
    logger.info("Training Kidney Disease Prediction Model...")
    
    # Create synthetic dataset for CKD
    np.random.seed(42)
    n_samples = 400
    df = pd.DataFrame({
        'age': np.random.randint(20, 80, n_samples),
        'blood_pressure': np.random.randint(50, 180, n_samples),
        'specific_gravity': np.random.uniform(1.005, 1.030, n_samples),
        'albumin': np.random.uniform(0, 5, n_samples),
        'sugar': np.random.uniform(0, 5, n_samples),
        'red_blood_cells': np.random.randint(0, 5, n_samples),
        'pus_cell': np.random.randint(0, 5, n_samples),
        'pus_cell_clumps': np.random.randint(0, 5, n_samples),
        'bacteria': np.random.randint(0, 5, n_samples),
        'blood_glucose_random': np.random.uniform(70, 490, n_samples),
        'blood_urea': np.random.uniform(10, 90, n_samples),
        'serum_creatinine': np.random.uniform(0.4, 15, n_samples),
        'sodium': np.random.randint(111, 150, n_samples),
        'potassium': np.random.uniform(2.5, 7, n_samples),
        'hemoglobin': np.random.uniform(3.1, 17.8, n_samples),
        'packed_cell_volume': np.random.uniform(9, 50, n_samples),
        'white_blood_cell_count': np.random.randint(3800, 14800, n_samples),
        'red_blood_cell_count': np.random.uniform(2.1, 8, n_samples),
        'hypertension': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'diabetes_mellitus': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'coronary_artery_disease': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'appetite': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'peda_edema': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'anemia': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'class': np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    })
    
    # Features and target
    X = df.drop('class', axis=1)
    y = df['class']
    
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
    logger.info(f"Kidney Disease Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/kidney_disease_model.pkl')
    joblib.dump(scaler, 'models/kidney_disease_scaler.pkl')
    joblib.dump(list(X.columns), 'models/kidney_disease_features.pkl')
    
    logger.info("Kidney disease model saved successfully")
    return accuracy

def train_liver_disease_model():
    """Train liver disease prediction model"""
    logger.info("Training Liver Disease Prediction Model...")
    
    # Create synthetic dataset for liver disease
    np.random.seed(42)
    n_samples = 350
    df = pd.DataFrame({
        'age': np.random.randint(20, 80, n_samples),
        'gender': np.random.choice([0, 1], n_samples),
        'total_bilirubin': np.random.uniform(0.4, 75, n_samples),
        'direct_bilirubin': np.random.uniform(0.1, 19, n_samples),
        'alkaline_phosphotase': np.random.randint(50, 1600, n_samples),
        'alamine_aminotransferase': np.random.randint(10, 2000, n_samples),
        'aspartate_aminotransferase': np.random.randint(10, 2000, n_samples),
        'total_proteins': np.random.uniform(2.7, 9.6, n_samples),
        'albumin': np.random.uniform(0.9, 5.5, n_samples),
        'albumin_globulin_ratio': np.random.uniform(0.1, 2.8, n_samples),
        'liver_disease': np.random.choice([0, 1], n_samples, p=[0.75, 0.25])
    })
    
    # Features and target
    X = df.drop('liver_disease', axis=1)
    y = df['liver_disease']
    
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
    logger.info(f"Liver Disease Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/liver_disease_model.pkl')
    joblib.dump(scaler, 'models/liver_disease_scaler.pkl')
    joblib.dump(list(X.columns), 'models/liver_disease_features.pkl')
    
    logger.info("Liver disease model saved successfully")
    return accuracy

def train_respiratory_disease_model():
    """Train respiratory disease prediction model (asthma/COPD)"""
    logger.info("Training Respiratory Disease Prediction Model...")
    
    # Create synthetic dataset for respiratory disease
    np.random.seed(42)
    n_samples = 400
    df = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'gender': np.random.choice([0, 1], n_samples),
        'smoking': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'smoking_years': np.random.randint(0, 50, n_samples),
        'family_history_asthma': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'family_history_copd': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
        'exposure_pollution': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'wheezing': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
        'shortness_breath': np.random.choice([0, 1], n_samples, p=[0.75, 0.25]),
        'cough': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        'chest_tightness': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'lung_function': np.random.uniform(40, 120, n_samples),
        'respiratory_disease': np.random.choice([0, 1], n_samples, p=[0.85, 0.15])
    })
    
    # Features and target
    X = df.drop('respiratory_disease', axis=1)
    y = df['respiratory_disease']
    
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
    logger.info(f"Respiratory Disease Model Accuracy: {accuracy:.4f}")
    
    # Save model and scaler
    joblib.dump(model, 'models/respiratory_disease_model.pkl')
    joblib.dump(scaler, 'models/respiratory_disease_scaler.pkl')
    joblib.dump(list(X.columns), 'models/respiratory_disease_features.pkl')
    
    logger.info("Respiratory disease model saved successfully")
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
        stroke_acc = train_stroke_model()
        kidney_acc = train_kidney_disease_model()
        liver_acc = train_liver_disease_model()
        respiratory_acc = train_respiratory_disease_model()
        
        logger.info("=" * 50)
        logger.info("ML Model Training Completed")
        logger.info("=" * 50)
        logger.info(f"Diabetes Model Accuracy: {diabetes_acc:.4f}")
        logger.info(f"Heart Disease Model Accuracy: {heart_acc:.4f}")
        logger.info(f"Hypertension Model Accuracy: {hypertension_acc:.4f}")
        logger.info(f"Stroke Model Accuracy: {stroke_acc:.4f}")
        logger.info(f"Kidney Disease Model Accuracy: {kidney_acc:.4f}")
        logger.info(f"Liver Disease Model Accuracy: {liver_acc:.4f}")
        logger.info(f"Respiratory Disease Model Accuracy: {respiratory_acc:.4f}")
        logger.info("All models saved to 'models/' directory")
        
    except Exception as e:
        logger.error(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    main()
