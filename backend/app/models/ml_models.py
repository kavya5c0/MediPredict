"""
ML Model Loader
Loads trained machine learning models for disease prediction
"""

import joblib
import numpy as np
import os
import logging

logger = logging.getLogger(__name__)

class MLModelLoader:
    def __init__(self):
        self.diabetes_model = None
        self.diabetes_scaler = None
        self.diabetes_features = None
        
        self.heart_disease_model = None
        self.heart_disease_scaler = None
        self.heart_disease_features = None
        
        self.hypertension_model = None
        self.hypertension_scaler = None
        self.hypertension_features = None
        
        self.load_models()
    
    def load_models(self):
        """Load all trained ML models"""
        try:
            # Load Diabetes Model
            if os.path.exists('models/diabetes_model.pkl'):
                self.diabetes_model = joblib.load('models/diabetes_model.pkl')
                self.diabetes_scaler = joblib.load('models/diabetes_scaler.pkl')
                self.diabetes_features = joblib.load('models/diabetes_features.pkl')
                logger.info("Diabetes model loaded successfully")
            
            # Load Heart Disease Model
            if os.path.exists('models/heart_disease_model.pkl'):
                self.heart_disease_model = joblib.load('models/heart_disease_model.pkl')
                self.heart_disease_scaler = joblib.load('models/heart_disease_scaler.pkl')
                self.heart_disease_features = joblib.load('models/heart_disease_features.pkl')
                logger.info("Heart disease model loaded successfully")
            
            # Load Hypertension Model
            if os.path.exists('models/hypertension_model.pkl'):
                self.hypertension_model = joblib.load('models/hypertension_model.pkl')
                self.hypertension_scaler = joblib.load('models/hypertension_scaler.pkl')
                self.hypertension_features = joblib.load('models/hypertension_features.pkl')
                logger.info("Hypertension model loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")
    
    def predict_diabetes(self, features):
        """Predict diabetes risk using ML model"""
        if not self.diabetes_model:
            return None
        
        try:
            # Map frontend field names to model feature names
            feature_dict = {
                'Pregnancies': features.get('pregnancies', 0) if 'pregnancies' in features else 0,
                'Glucose': features.get('glucose_level', 100),
                'BloodPressure': features.get('blood_pressure_systolic', 120),
                'SkinThickness': features.get('skin_thickness', 20) if 'skin_thickness' in features else 20,
                'Insulin': features.get('insulin', 80) if 'insulin' in features else 80,
                'BMI': float(features.get('bmi', 25)) if features.get('bmi') else 25,
                'DiabetesPedigreeFunction': features.get('diabetes_pedigree', 0.5) if 'diabetes_pedigree' in features else 0.5,
                'Age': int(features.get('age', 30))
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.diabetes_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.diabetes_scaler.transform(feature_array)
            
            # Predict
            prediction = self.diabetes_model.predict(feature_scaled)[0]
            probability = self.diabetes_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting diabetes: {e}")
            return None
    
    def predict_heart_disease(self, features):
        """Predict heart disease risk using ML model"""
        if not self.heart_disease_model:
            return None
        
        try:
            # Map frontend field names to model feature names
            feature_dict = {
                'age': int(features.get('age', 45)),
                'sex': 1 if features.get('sex') == 'male' else 0,
                'cp': 0,  # chest pain type - default
                'trestbps': int(features.get('blood_pressure_systolic', 120)),
                'chol': int(features.get('cholesterol', 200)),
                'fbs': 1 if float(features.get('glucose_level', 100)) > 120 else 0,  # fasting blood sugar
                'restecg': 0,  # resting ECG - default
                'thalach': int(features.get('heart_rate', 75)),
                'exang': 0,  # exercise angina - default
                'oldpeak': 1.0,  # ST depression - default
                'slope': 1,  # ST slope - default
                'ca': 0,  # major vessels - default
                'thal': 1  # thalassemia - default
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.heart_disease_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.heart_disease_scaler.transform(feature_array)
            
            # Predict
            prediction = self.heart_disease_model.predict(feature_scaled)[0]
            probability = self.heart_disease_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting heart disease: {e}")
            return None
    
    def predict_hypertension(self, features):
        """Predict hypertension risk using ML model"""
        if not self.hypertension_model:
            return None
        
        try:
            # Create feature array
            feature_dict = {
                'age': features.get('age', 45),
                'bmi': features.get('bmi', 25),
                'systolic_bp': features.get('systolic_bp', 120),
                'diastolic_bp': features.get('diastolic_bp', 80),
                'cholesterol': features.get('cholesterol', 200),
                'physical_activity': features.get('physical_activity', 150),
                'smoking': features.get('smoking', 0),
                'family_history': features.get('family_history', 0)
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.hypertension_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.hypertension_scaler.transform(feature_array)
            
            # Predict
            prediction = self.hypertension_model.predict(feature_scaled)[0]
            probability = self.hypertension_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting hypertension: {e}")
            return None

# Global ML model loader instance
ml_models = MLModelLoader()
