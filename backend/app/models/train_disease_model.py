import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from app.models.disease_model import DiseasePredictor
import joblib

def generate_synthetic_data(n_samples=1000):
    """Generate synthetic health data for training"""
    np.random.seed(42)
    
    data = []
    labels = []
    
    disease_labels = [
        "Diabetes", "Heart Disease", "Hypertension", 
        "Asthma", "COPD", "Arthritis", 
        "Depression", "Anxiety", "Obesity", "Cancer"
    ]
    
    for _ in range(n_samples):
        # Generate random health parameters
        age = np.random.randint(18, 80)
        bmi = np.random.normal(25, 5)
        bp_systolic = np.random.normal(120, 20)
        bp_diastolic = np.random.normal(80, 10)
        heart_rate = np.random.normal(72, 10)
        glucose = np.random.normal(100, 30)
        cholesterol = np.random.normal(200, 40)
        smoking = np.random.choice([0, 1], p=[0.7, 0.3])
        alcohol = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # Family history
        family_diabetes = np.random.choice([0, 1], p=[0.8, 0.2])
        family_heart = np.random.choice([0, 1], p=[0.85, 0.15])
        family_hypertension = np.random.choice([0, 1], p=[0.8, 0.2])
        
        # Lifestyle
        physical_activity = np.random.randint(0, 300)
        sleep_hours = np.random.normal(7, 1.5)
        stress_level = np.random.randint(1, 11)
        
        # Existing conditions
        diabetes = np.random.choice([0, 1], p=[0.9, 0.1])
        heart_disease = np.random.choice([0, 1], p=[0.95, 0.05])
        hypertension = np.random.choice([0, 1], p=[0.85, 0.15])
        asthma = np.random.choice([0, 1], p=[0.9, 0.1])
        arthritis = np.random.choice([0, 1], p=[0.85, 0.15])
        
        features = [
            age, bmi, bp_systolic, bp_diastolic, heart_rate, glucose, cholesterol,
            smoking, alcohol, family_diabetes, family_heart, family_hypertension,
            physical_activity, sleep_hours, stress_level, diabetes, heart_disease,
            hypertension, asthma, arthritis
        ]
        
        # Assign label based on features (simplified logic)
        if glucose > 126 or family_diabetes:
            label = 0  # Diabetes
        elif bp_systolic > 140 or family_heart:
            label = 1  # Heart Disease
        elif bp_diastolic > 90 or family_hypertension:
            label = 2  # Hypertension
        elif asthma:
            label = 3  # Asthma
        elif smoking and age > 50:
            label = 4  # COPD
        elif arthritis:
            label = 5  # Arthritis
        elif stress_level > 7:
            label = 6  # Depression
        elif stress_level > 6:
            label = 7  # Anxiety
        elif bmi > 30:
            label = 8  # Obesity
        else:
            label = np.random.randint(0, 10)
        
        data.append(features)
        labels.append(label)
    
    return np.array(data), np.array(labels)

def train_model():
    """Train the disease prediction model"""
    print("Generating synthetic training data...")
    X, y = generate_synthetic_data(n_samples=5000)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save scaler
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Convert to PyTorch tensors
    X_train_tensor = torch.FloatTensor(X_train_scaled)
    y_train_tensor = torch.LongTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test_scaled)
    y_test_tensor = torch.LongTensor(y_test)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    # Initialize model
    input_size = X_train.shape[1]
    num_classes = 10
    
    predictor = DiseasePredictor()
    model = predictor.create_model(input_size, num_classes)
    
    # Training
    print("Training model...")
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    num_epochs = 50
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {total_loss/len(train_loader):.4f}')
    
    # Evaluate
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        _, predicted = torch.max(test_outputs.data, 1)
        
        accuracy = (predicted == y_test_tensor).sum().item() / len(y_test_tensor)
        print(f'Test Accuracy: {accuracy:.2f}')
    
    # Save model
    import os
    os.makedirs('models', exist_ok=True)
    torch.save(model.state_dict(), 'models/disease_prediction.pth')
    print("Model saved to models/disease_prediction.pth")
    
    return model

if __name__ == "__main__":
    train_model()
