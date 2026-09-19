"""
Lightweight disease prediction model using scikit-learn instead of PyTorch
Optimized for free-tier deployment (reduced memory footprint)
"""
import numpy as np
from typing import List, Dict
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class DiseasePredictorLite:
    """Lightweight disease predictor using scikit-learn instead of PyTorch"""
    
    def __init__(self, model_path: str = None, scaler_path: str = None):
        self.model = None
        self.scaler = None
        self.disease_labels = [
            "Diabetes", "Heart Disease", "Hypertension", 
            "Asthma", "COPD", "Arthritis", 
            "Depression", "Anxiety", "Obesity", "Cancer"
        ]
        
        if model_path:
            self.load_model(model_path, scaler_path)
        else:
            # Create a simple model for demonstration
            self.create_simple_model()
    
    def create_simple_model(self):
        """Create a simple RandomForest model for demonstration"""
        self.model = RandomForestClassifier(
            n_estimators=50,  # Reduced for memory
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
        # Train with dummy data for demonstration
        # In production, you would train with real data
        X_dummy = np.random.rand(100, 20)  # 20 features
        y_dummy = np.random.randint(0, 10, 100)  # 10 classes
        
        X_scaled = self.scaler.fit_transform(X_dummy)
        self.model.fit(X_scaled, y_dummy)
    
    def load_model(self, model_path: str, scaler_path: str = None):
        """Load trained model from disk"""
        try:
            self.model = joblib.load(model_path)
            if scaler_path:
                self.scaler = joblib.load(scaler_path)
            else:
                self.scaler = StandardScaler()
        except Exception as e:
            print(f"Failed to load model: {e}, creating simple model")
            self.create_simple_model()
    
    def predict(self, features: List[float]) -> Dict:
        """Predict disease from features"""
        if not self.model:
            raise ValueError("Model not initialized")
        
        try:
            features_array = np.array(features).reshape(1, -1)
            
            # Ensure we have 20 features (pad or truncate if needed)
            if features_array.shape[1] < 20:
                features_array = np.pad(features_array, ((0, 0), (0, 20 - features_array.shape[1])), 'constant')
            elif features_array.shape[1] > 20:
                features_array = features_array[:, :20]
            
            if self.scaler:
                features_array = self.scaler.transform(features_array)
            
            # Get prediction and probabilities
            predicted_class = self.model.predict(features_array)[0]
            probabilities = self.model.predict_proba(features_array)[0]
            confidence = probabilities[predicted_class]
            
            result = {
                "predicted_disease": self.disease_labels[predicted_class],
                "confidence": float(confidence),
                "all_probabilities": {
                    label: float(prob) 
                    for label, prob in zip(self.disease_labels, probabilities)
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Prediction failed: {e}")
            # Return fallback prediction
            return {
                "predicted_disease": "General Health Check",
                "confidence": 0.5,
                "all_probabilities": {label: 0.1 for label in self.disease_labels},
                "error": str(e)
            }
    
    def train(self, X_train, y_train):
        """Train the model with data"""
        if not self.model:
            self.create_simple_model()
        
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        
        return self.model