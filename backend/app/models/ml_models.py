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
        
        self.stroke_model = None
        self.stroke_scaler = None
        self.stroke_features = None
        
        self.kidney_disease_model = None
        self.kidney_disease_scaler = None
        self.kidney_disease_features = None
        
        self.liver_disease_model = None
        self.liver_disease_scaler = None
        self.liver_disease_features = None
        
        self.respiratory_disease_model = None
        self.respiratory_disease_scaler = None
        self.respiratory_disease_features = None
        
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
            
            # Load Stroke Model
            if os.path.exists('models/stroke_model.pkl'):
                self.stroke_model = joblib.load('models/stroke_model.pkl')
                self.stroke_scaler = joblib.load('models/stroke_scaler.pkl')
                self.stroke_features = joblib.load('models/stroke_features.pkl')
                logger.info("Stroke model loaded successfully")
            
            # Load Kidney Disease Model
            if os.path.exists('models/kidney_disease_model.pkl'):
                self.kidney_disease_model = joblib.load('models/kidney_disease_model.pkl')
                self.kidney_disease_scaler = joblib.load('models/kidney_disease_scaler.pkl')
                self.kidney_disease_features = joblib.load('models/kidney_disease_features.pkl')
                logger.info("Kidney disease model loaded successfully")
            
            # Load Liver Disease Model
            if os.path.exists('models/liver_disease_model.pkl'):
                self.liver_disease_model = joblib.load('models/liver_disease_model.pkl')
                self.liver_disease_scaler = joblib.load('models/liver_disease_scaler.pkl')
                self.liver_disease_features = joblib.load('models/liver_disease_features.pkl')
                logger.info("Liver disease model loaded successfully")
            
            # Load Respiratory Disease Model
            if os.path.exists('models/respiratory_disease_model.pkl'):
                self.respiratory_disease_model = joblib.load('models/respiratory_disease_model.pkl')
                self.respiratory_disease_scaler = joblib.load('models/respiratory_disease_scaler.pkl')
                self.respiratory_disease_features = joblib.load('models/respiratory_disease_features.pkl')
                logger.info("Respiratory disease model loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading ML models: {e}")
    
    def predict_diabetes(self, features):
        """Predict diabetes risk using ML model"""
        if not self.diabetes_model:
            logger.warning("Diabetes model not loaded")
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
            
            logger.info(f"Diabetes features: {feature_dict}")
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.diabetes_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.diabetes_scaler.transform(feature_array)
            
            # Predict
            prediction = self.diabetes_model.predict(feature_scaled)[0]
            probability = self.diabetes_model.predict_proba(feature_scaled)[0][1]
            
            logger.info(f"Diabetes prediction: {prediction}, probability: {probability}")
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting diabetes: {e}", exc_info=True)
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
    
    def predict_stroke(self, features):
        """Predict stroke risk using ML model"""
        if not self.stroke_model:
            return None
        
        try:
            # Create feature array
            feature_dict = {
                'age': int(features.get('age', 50)),
                'gender': 1 if features.get('gender') == 'male' else 0,
                'hypertension': 1 if features.get('blood_pressure_systolic', 120) >= 140 else 0,
                'heart_disease': 1 if features.get('heart_disease', False) else 0,
                'ever_married': 1 if features.get('marital_status') == 'married' else 0,
                'work_type': 0,  # default
                'residence_type': 0,  # default
                'avg_glucose_level': float(features.get('glucose_level', 100)),
                'bmi': float(features.get('bmi', 25)),
                'smoking_status': 1 if features.get('smoking', False) else 0
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.stroke_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.stroke_scaler.transform(feature_array)
            
            # Predict
            prediction = self.stroke_model.predict(feature_scaled)[0]
            probability = self.stroke_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting stroke: {e}")
            return None
    
    def predict_kidney_disease(self, features):
        """Predict kidney disease risk using ML model"""
        if not self.kidney_disease_model:
            return None
        
        try:
            # Create feature array (using subset of available features)
            feature_dict = {
                'age': int(features.get('age', 50)),
                'blood_pressure': int(features.get('blood_pressure_systolic', 120)),
                'specific_gravity': 1.015,  # default normal value
                'albumin': 0,  # default
                'sugar': 1 if float(features.get('glucose_level', 100)) > 120 else 0,
                'red_blood_cells': 0,  # default
                'pus_cell': 0,  # default
                'pus_cell_clumps': 0,  # default
                'bacteria': 0,  # default
                'blood_glucose_random': float(features.get('glucose_level', 100)),
                'blood_urea': 30,  # default
                'serum_creatinine': 1.0,  # default
                'sodium': 140,  # default
                'potassium': 4.0,  # default
                'hemoglobin': 14,  # default
                'packed_cell_volume': 40,  # default
                'white_blood_cell_count': 7500,  # default
                'red_blood_cell_count': 4.5,  # default
                'hypertension': 1 if features.get('blood_pressure_systolic', 120) >= 140 else 0,
                'diabetes_mellitus': 1 if float(features.get('glucose_level', 100)) > 126 else 0,
                'coronary_artery_disease': 0,  # default
                'appetite': 1,  # default
                'peda_edema': 0,  # default
                'anemia': 0  # default
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.kidney_disease_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.kidney_disease_scaler.transform(feature_array)
            
            # Predict
            prediction = self.kidney_disease_model.predict(feature_scaled)[0]
            probability = self.kidney_disease_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting kidney disease: {e}")
            return None
    
    def predict_liver_disease(self, features):
        """Predict liver disease risk using ML model"""
        if not self.liver_disease_model:
            return None
        
        try:
            # Create feature array
            feature_dict = {
                'age': int(features.get('age', 50)),
                'gender': 1 if features.get('gender') == 'male' else 0,
                'total_bilirubin': 1.0,  # default
                'direct_bilirubin': 0.3,  # default
                'alkaline_phosphotase': 100,  # default
                'alamine_aminotransferase': 30,  # default
                'aspartate_aminotransferase': 30,  # default
                'total_proteins': 7.0,  # default
                'albumin': 4.0,  # default
                'albumin_globulin_ratio': 1.0  # default
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.liver_disease_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.liver_disease_scaler.transform(feature_array)
            
            # Predict
            prediction = self.liver_disease_model.predict(feature_scaled)[0]
            probability = self.liver_disease_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting liver disease: {e}")
            return None
    
    def predict_respiratory_disease(self, features):
        """Predict respiratory disease risk using ML model"""
        if not self.respiratory_disease_model:
            return None
        
        try:
            # Create feature array
            feature_dict = {
                'age': int(features.get('age', 50)),
                'gender': 1 if features.get('gender') == 'male' else 0,
                'smoking': 1 if features.get('smoking', False) else 0,
                'smoking_years': int(features.get('age', 50)) - 20 if features.get('smoking', False) else 0,
                'family_history_asthma': 1 if features.get('family_history_asthma', False) else 0,
                'family_history_copd': 1 if features.get('family_history_copd', False) else 0,
                'exposure_pollution': 0,  # default
                'wheezing': 0,  # default
                'shortness_breath': 0,  # default
                'cough': 0,  # default
                'chest_tightness': 0,  # default
                'lung_function': 100  # default
            }
            
            # Order features correctly
            feature_array = np.array([feature_dict[feat] for feat in self.respiratory_disease_features]).reshape(1, -1)
            
            # Scale features
            feature_scaled = self.respiratory_disease_scaler.transform(feature_array)
            
            # Predict
            prediction = self.respiratory_disease_model.predict(feature_scaled)[0]
            probability = self.respiratory_disease_model.predict_proba(feature_scaled)[0][1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': 'High' if probability > 0.7 else 'Medium' if probability > 0.4 else 'Low'
            }
        except Exception as e:
            logger.error(f"Error predicting respiratory disease: {e}")
            return None

# Global ML model loader instance
ml_models = MLModelLoader()
