import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict
import joblib

class DiseasePredictionModel(nn.Module):
    def __init__(self, input_size: int, hidden_size: int = 128, num_classes: int = 10):
        super(DiseasePredictionModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, num_classes)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
        self.batch_norm1 = nn.BatchNorm1d(hidden_size)
        self.batch_norm2 = nn.BatchNorm1d(hidden_size // 2)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.batch_norm1(x)
        x = self.relu(x)
        x = self.dropout(x)
        
        x = self.fc2(x)
        x = self.batch_norm2(x)
        x = self.relu(x)
        x = self.dropout(x)
        
        x = self.fc3(x)
        return x

class DiseasePredictor:
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
    
    def create_model(self, input_size: int, num_classes: int = 10):
        self.model = DiseasePredictionModel(input_size, num_classes=num_classes)
        return self.model
    
    def load_model(self, model_path: str, scaler_path: str = None):
        self.model = DiseasePredictionModel(input_size=20, num_classes=10)
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()
        
        if scaler_path:
            self.scaler = joblib.load(scaler_path)
    
    def predict(self, features: List[float]) -> Dict:
        if not self.model:
            raise ValueError("Model not loaded")
        
        features_array = np.array(features).reshape(1, -1)
        
        if self.scaler:
            features_array = self.scaler.transform(features_array)
        
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features_array)
            outputs = self.model(features_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        result = {
            "predicted_disease": self.disease_labels[predicted_class],
            "confidence": confidence,
            "all_probabilities": {
                label: prob.item() 
                for label, prob in zip(self.disease_labels, probabilities[0])
            }
        }
        
        return result
    
    def train(self, X_train, y_train, epochs: int = 100, batch_size: int = 32):
        if not self.model:
            raise ValueError("Model not created")
        
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        
        X_tensor = torch.FloatTensor(X_train)
        y_tensor = torch.LongTensor(y_train)
        
        self.model.train()
        for epoch in range(epochs):
            for i in range(0, len(X_train), batch_size):
                batch_X = X_tensor[i:i+batch_size]
                batch_y = y_tensor[i:i+batch_size]
                
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()
        
        return self.model
