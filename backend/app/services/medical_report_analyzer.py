import pytesseract
import cv2
import numpy as np
from PIL import Image
from typing import Dict, List
import re

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Transformers not available, using basic analysis")

try:
    import spacy
    SPACY_AVAILABLE = True
    try:
        NLP = spacy.load("en_core_web_sm")
    except:
        SPACY_AVAILABLE = False
        print("spaCy model not available")
except ImportError:
    SPACY_AVAILABLE = False
    print("spaCy not available, using basic analysis")

class MedicalReportAnalyzer:
    def __init__(self):
        self.nlp = NLP if SPACY_AVAILABLE else None
        self.medical_ner = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                self.medical_ner = pipeline(
                    "ner",
                    model="samrawat/bert-base-uncased-medical-ner",
                    aggregation_strategy="simple"
                )
            except Exception as e:
                print(f"Failed to load medical NER model: {e}")
        
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from medical report image using OCR"""
        try:
            image = cv2.imread(image_path)
            
            # Preprocessing
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            gray = cv2.medianBlur(gray, 3)
            
            # OCR
            text = pytesseract.image_to_string(gray)
            return text
        except Exception as e:
            print(f"OCR failed: {e}")
            return ""
    
    def extract_medical_entities(self, text: str) -> Dict:
        """Extract medical entities from text using NER"""
        medical_info = {
            "diseases": [],
            "medications": [],
            "symptoms": [],
            "lab_values": [],
            "vitals": []
        }
        
        if self.medical_ner:
            try:
                entities = self.medical_ner(text)
                
                for entity in entities:
                    label = entity['entity_group']
                    word = entity['word']
                    
                    if label in ['DISEASE', 'CONDITION']:
                        medical_info["diseases"].append(word)
                    elif label in ['MEDICATION', 'DRUG']:
                        medical_info["medications"].append(word)
                    elif label in ['SYMPTOM']:
                        medical_info["symptoms"].append(word)
            except Exception as e:
                print(f"NER extraction failed: {e}")
        else:
            # Fallback: basic keyword matching
            text_lower = text.lower()
            common_diseases = ['diabetes', 'hypertension', 'asthma', 'arthritis', 'cancer', 'heart disease', 'copd']
            for disease in common_diseases:
                if disease in text_lower:
                    medical_info["diseases"].append(disease.title())
        
        # Extract lab values using regex
        lab_pattern = r'(\w+)\s*[:=]\s*(\d+\.?\d*)\s*(\w*/?\w*)'
        lab_matches = re.findall(lab_pattern, text)
        
        for match in lab_matches:
            medical_info["lab_values"].append({
                "test": match[0],
                "value": match[1],
                "unit": match[2]
            })
        
        # Extract vitals
        vital_patterns = {
            "blood_pressure": r'BP\s*[:=]\s*(\d+/\d+)',
            "heart_rate": r'HR\s*[:=]\s*(\d+)',
            "temperature": r'Temp\s*[:=]\s*(\d+\.?\d*)',
            "weight": r'Weight\s*[:=]\s*(\d+\.?\d*)\s*(kg|lbs)',
            "height": r'Height\s*[:=]\s*(\d+\.?\d*)\s*(cm|ft|m)'
        }
        
        for vital, pattern in vital_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                medical_info["vitals"].append({
                    "type": vital,
                    "value": match.group(1)
                })
        
        return medical_info
    
    def analyze_report(self, image_path: str = None, text: str = None) -> Dict:
        """Analyze medical report from image or text"""
        if image_path:
            text = self.extract_text_from_image(image_path)
        
        if not text:
            return {"error": "No text provided"}
        
        medical_entities = self.extract_medical_entities(text)
        
        # Sentiment analysis for report tone
        sentiment = "neutral"
        if self.nlp:
            try:
                doc = self.nlp(text)
                if hasattr(doc, '_.sentiment'):
                    if doc._.sentiment > 0:
                        sentiment = "positive"
                    elif doc._.sentiment < 0:
                        sentiment = "negative"
            except Exception as e:
                print(f"Sentiment analysis failed: {e}")
        
        # Summary generation
        summary = self._generate_summary(medical_entities)
        
        return {
            "extracted_text": text,
            "medical_entities": medical_entities,
            "sentiment": sentiment,
            "summary": summary,
            "recommendations": self._generate_recommendations(medical_entities)
        }
    
    def _generate_summary(self, medical_entities: Dict) -> str:
        """Generate a summary of the medical report"""
        summary_parts = []
        
        if medical_entities["diseases"]:
            summary_parts.append(f"Detected conditions: {', '.join(medical_entities['diseases'])}")
        
        if medical_entities["medications"]:
            summary_parts.append(f"Current medications: {', '.join(medical_entities['medications'])}")
        
        if medical_entities["symptoms"]:
            summary_parts.append(f"Reported symptoms: {', '.join(medical_entities['symptoms'])}")
        
        if medical_entities["lab_values"]:
            summary_parts.append(f"Lab tests performed: {len(medical_entities['lab_values'])}")
        
        return ". ".join(summary_parts) if summary_parts else "No significant medical information detected."
    
    def _generate_recommendations(self, medical_entities: Dict) -> List[str]:
        """Generate health recommendations based on extracted data"""
        recommendations = []
        
        if "Diabetes" in medical_entities["diseases"]:
            recommendations.append("Monitor blood sugar regularly")
            recommendations.append("Follow diabetic diet guidelines")
        
        if "Hypertension" in medical_entities["diseases"]:
            recommendations.append("Monitor blood pressure daily")
            recommendations.append("Reduce sodium intake")
        
        if any("high" in str(vital["value"]).lower() for vital in medical_entities["vitals"]):
            recommendations.append("Consult with healthcare provider about elevated values")
        
        if not recommendations:
            recommendations.append("Continue regular health check-ups")
            recommendations.append("Maintain healthy lifestyle")
        
        return recommendations
