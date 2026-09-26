"""
Real Medical Report Analysis System
Based on actual medical terminology, ICD codes, and clinical practice
"""

# Real ICD-10 Codes for common conditions
ICD_CODES = {
    "diabetes": {
        "type1": "E10",
        "type2": "E11",
        "prediabetes": "R73.03",
        "complications": {
            "nephropathy": "E11.2",
            "retinopathy": "E11.3",
            "neuropathy": "E11.4",
            "circulatory": "E11.5"
        }
    },
    "hypertension": {
        "essential": "I10",
        "secondary": "I15",
        "complications": {
            "heart": "I11",
            "kidney": "I12",
            "brain": "I60-I69"
        }
    },
    "cardiovascular": {
        "angina": "I20",
        "heart_attack": "I21-I22",
        "heart_failure": "I50",
        "arrhythmia": "I47-I49"
    },
    "obesity": {
        "bmi_30_34": "E66.0",
        "bmi_35_39": "E66.1",
        "bmi_40_plus": "E66.2"
    }
}

# Real medical terminology
MEDICAL_TERMINOLOGY = {
    "blood_tests": {
        "hemoglobin_a1c": {
            "normal": "4.8-5.6%",
            "prediabetes": "5.7-6.4%",
            "diabetes": "6.5% or higher",
            "clinical_significance": "Average blood glucose over past 2-3 months"
        },
        "fasting_blood_glucose": {
            "normal": "70-99 mg/dL",
            "prediabetes": "100-125 mg/dL",
            "diabetes": "126 mg/dL or higher",
            "clinical_significance": "Blood glucose after 8+ hours fasting"
        },
        "lipid_panel": {
            "total_cholesterol": {
                "desirable": "< 200 mg/dL",
                "borderline": "200-239 mg/dL",
                "high": "≥ 240 mg/dL"
            },
            "ldl": {
                "optimal": "< 100 mg/dL",
                "near_optimal": "100-129 mg/dL",
                "borderline": "130-159 mg/dL",
                "high": "160-189 mg/dL",
                "very_high": "≥ 190 mg/dL"
            },
            "hdl": {
                "men_low": "< 40 mg/dL",
                "women_low": "< 50 mg/dL",
                "optimal": "≥ 60 mg/dL"
            },
            "triglycerides": {
                "normal": "< 150 mg/dL",
                "borderline": "150-199 mg/dL",
                "high": "200-499 mg/dL",
                "very_high": "≥ 500 mg/dL"
            }
        },
        "liver_function": {
            "alt": {
                "normal": "7-56 U/L",
                "elevated": "> 56 U/L",
                "significance": "Liver enzyme, elevated in liver damage"
            },
            "ast": {
                "normal": "10-40 U/L",
                "elevated": "> 40 U/L",
                "significance": "Liver enzyme, elevated in liver or muscle damage"
            }
        },
        "kidney_function": {
            "creatinine": {
                "men": "0.74-1.35 mg/dL",
                "women": "0.59-1.04 mg/dL",
                "significance": "Kidney function marker"
            },
            "gfr": {
                "normal": "≥ 60 mL/min",
                "kidney_disease": "< 60 mL/min",
                "significance": "Glomerular filtration rate"
            }
        }
    },
    "imaging": {
        "chest_xray": {
            "normal": "Clear lung fields, normal heart size, no consolidation",
            "abnormalities": [
                "consolidation - pneumonia",
                "cardiomegaly - enlarged heart",
                "pulmonary edema - fluid in lungs",
                "pleural effusion - fluid around lungs"
            ]
        },
        "ecg": {
            "normal": "Sinus rhythm, normal intervals, no ST changes",
            "abnormalities": [
                "sinus tachycardia - HR > 100",
                "sinus bradycardia - HR < 60",
                "atrial fibrillation - irregular rhythm",
                "ST elevation - possible heart attack",
                "T wave inversion - ischemia"
            ]
        }
    }
}

# Real medical report templates
MEDICAL_REPORT_TEMPLATES = {
    "lab_report": {
        "patient_info": "Patient Name, DOB, MRN",
        "specimen": "Type of specimen, collection date/time",
        "tests": "List of tests with results and reference ranges",
        "clinical_significance": "Interpretation of abnormal results",
        "physician_signature": "Attending physician information"
    },
    "radiology_report": {
        "clinical_indication": "Reason for imaging",
        "technique": "Imaging method used",
        "findings": "Detailed observations",
        "impression": "Summary and diagnosis",
        "radiologist_signature": "Radiologist information"
    },
    "progress_note": {
        "subjective": "Patient symptoms and concerns",
        "objective": "Vital signs, physical exam findings",
        "assessment": "Diagnosis and condition status",
        "plan": "Treatment plan and next steps"
    }
}

# Real sample medical reports based on actual clinical cases
SAMPLE_MEDICAL_REPORTS = {
    "diabetes_case": {
        "type": "Laboratory Report",
        "patient_data": {
            "age": 52,
            "gender": "Male",
            "complaints": "Increased thirst, frequent urination, fatigue"
        },
        "lab_results": {
            "hemoglobin_a1c": "7.8%",
            "fasting_glucose": "142 mg/dL",
            "random_glucose": "198 mg/dL",
            "total_cholesterol": "245 mg/dL",
            "ldl": "162 mg/dL",
            "hdl": "38 mg/dL",
            "triglycerides": "210 mg/dL"
        },
        "interpretation": {
            "primary_diagnosis": "Type 2 Diabetes Mellitus (ICD-10: E11)",
            "secondary_diagnosis": "Dyslipidemia (ICD-10: E78.5)",
            "clinical_significance": "Elevated A1c and glucose consistent with uncontrolled diabetes. Lipid profile shows increased cardiovascular risk.",
            "recommendations": [
                "Initiate metformin therapy",
                "Refer to diabetes educator",
                "Cardiovascular risk reduction program",
                "Follow-up A1c in 3 months"
            ]
        }
    },
    "hypertension_case": {
        "type": "Clinical Progress Note",
        "patient_data": {
            "age": 58,
            "gender": "Female",
            "complaints": "Headaches, occasional dizziness"
        },
        "vital_signs": {
            "blood_pressure": "152/94 mmHg",
            "heart_rate": "78 bpm",
            "bmi": "29.4"
        },
        "findings": {
            "blood_pressure_stage": "Stage 2 Hypertension (ICD-10: I10)",
            "risk_factors": [
                "Age > 55",
                "BMI in overweight range",
                "Family history of hypertension"
            ],
            "target_organ_damage": "None detected"
        },
        "plan": [
            "Initiate ACE inhibitor therapy",
            "DASH diet counseling",
            "Home blood pressure monitoring",
            "Sodium restriction < 2,300 mg/day",
            "Follow-up in 2 weeks"
        ]
    },
    "cardiovascular_case": {
        "type": "Cardiology Consultation",
        "patient_data": {
            "age": 65,
            "gender": "Male",
            "complaints": "Chest pain during exertion, shortness of breath"
        },
        "test_results": {
            "ecg": "Sinus rhythm, ST depression in leads V4-V6",
            "echocardiogram": "Ejection fraction 52%, mild left ventricular hypertrophy",
            "stress_test": "Positive for ischemia at 6 METs",
            "lipid_panel": {
                "total_cholesterol": "268 mg/dL",
                "ldl": "185 mg/dL",
                "hdl": "42 mg/dL",
                "triglycerides": "205 mg/dL"
            }
        },
        "diagnosis": {
            "primary": "Stable Angina (ICD-10: I20)",
            "secondary": "Coronary Artery Disease (ICD-10: I25)",
            "risk_stratification": "Intermediate risk"
        },
        "recommendations": [
            "Initiate aspirin therapy",
            "High-intensity statin therapy",
            "Beta-blocker for symptom control",
            "Cardiac stress testing annually",
            "Consider cardiac catheterization if symptoms worsen"
        ]
    }
}

def analyze_medical_text(text: str) -> dict:
    """Analyze medical text using real medical terminology and patterns"""
    text_lower = text.lower()
    analysis = {
        "key_findings": [],
        "medical_entities": [],
        "potential_conditions": [],
        "lab_values": {},
        "clinical_significance": "",
        "recommendations": []
    }
    
    # Extract lab values using regex patterns
    import re
    
    # Blood glucose patterns
    glucose_match = re.search(r'glucose[:\s]*(\d+)\s*mg/dL', text_lower)
    if glucose_match:
        glucose_value = int(glucose_match.group(1))
        analysis["lab_values"]["glucose"] = f"{glucose_value} mg/dL"
        if glucose_value >= 126:
            analysis["potential_conditions"].append("Diabetes Mellitus (ICD-10: E11)")
            analysis["key_findings"].append(f"Elevated fasting glucose ({glucose_value} mg/dL) consistent with diabetes")
        elif glucose_value >= 100:
            analysis["potential_conditions"].append("Prediabetes (ICD-10: R73.03)")
            analysis["key_findings"].append(f"Glucose in prediabetic range ({glucose_value} mg/dL)")
    
    # A1c patterns
    a1c_match = re.search(r'a1c|hba1c|hemoglobin a1c[:\s]*([\d.]+)%', text_lower)
    if a1c_match:
        a1c_value = float(a1c_match.group(1))
        analysis["lab_values"]["a1c"] = f"{a1c_value}%"
        if a1c_value >= 6.5:
            analysis["potential_conditions"].append("Diabetes Mellitus (ICD-10: E11)")
            analysis["key_findings"].append(f"Elevated A1c ({a1c_value}%) indicates poor glycemic control")
        elif a1c_value >= 5.7:
            analysis["potential_conditions"].append("Prediabetes (ICD-10: R73.03)")
            analysis["key_findings"].append(f"A1c in prediabetic range ({a1c_value}%)")
    
    # Blood pressure patterns
    bp_match = re.search(r'blood pressure|bp[:\s]*(\d+)/(\d+)\s*mmhg', text_lower)
    if bp_match:
        systolic = int(bp_match.group(1))
        diastolic = int(bp_match.group(2))
        analysis["lab_values"]["blood_pressure"] = f"{systolic}/{diastolic} mmHg"
        
        if systolic >= 140 or diastolic >= 90:
            analysis["potential_conditions"].append("Stage 2 Hypertension (ICD-10: I10)")
            analysis["key_findings"].append(f"Stage 2 hypertension ({systolic}/{diastolic} mmHg)")
        elif systolic >= 130 or diastolic >= 80:
            analysis["potential_conditions"].append("Stage 1 Hypertension (ICD-10: I10)")
            analysis["key_findings"].append(f"Stage 1 hypertension ({systolic}/{diastolic} mmHg)")
        elif systolic >= 120:
            analysis["potential_conditions"].append("Elevated Blood Pressure")
            analysis["key_findings"].append(f"Elevated blood pressure ({systolic}/{diastolic} mmHg)")
    
    # Cholesterol patterns
    cholesterol_match = re.search(r'cholesterol[:\s]*(\d+)\s*mg/dL', text_lower)
    if cholesterol_match:
        cholesterol_value = int(cholesterol_match.group(1))
        analysis["lab_values"]["cholesterol"] = f"{cholesterol_value} mg/dL"
        if cholesterol_value >= 240:
            analysis["potential_conditions"].append("Hypercholesterolemia (ICD-10: E78.5)")
            analysis["key_findings"].append(f"High total cholesterol ({cholesterol_value} mg/dL)")
        elif cholesterol_value >= 200:
            analysis["key_findings"].append(f"Borderline high cholesterol ({cholesterol_value} mg/dL)")
    
    # BMI patterns
    bmi_match = re.search(r'bmi[:\s]*([\d.]+)', text_lower)
    if bmi_match:
        bmi_value = float(bmi_match.group(1))
        analysis["lab_values"]["bmi"] = f"{bmi_value}"
        if bmi_value >= 30:
            analysis["potential_conditions"].append("Obesity (ICD-10: E66)")
            analysis["key_findings"].append(f"Obesity (BMI {bmi_value})")
        elif bmi_value >= 25:
            analysis["potential_conditions"].append("Overweight")
            analysis["key_findings"].append(f"Overweight (BMI {bmi_value})")
    
    # Extract symptoms
    symptoms = {
        "chest pain": "Possible cardiac issue",
        "shortness of breath": "Possible cardiac or respiratory issue",
        "headache": "Various causes including hypertension",
        "dizziness": "Possible cardiovascular or neurological issue",
        "fatigue": "Multiple possible causes",
        "increased thirst": "Possible diabetes",
        "frequent urination": "Possible diabetes",
        "blurred vision": "Possible diabetes complication"
    }
    
    for symptom, significance in symptoms.items():
        if symptom in text_lower:
            analysis["medical_entities"].append({
                "type": "symptom",
                "text": symptom,
                "significance": significance
            })
    
    # Generate clinical significance
    if analysis["potential_conditions"]:
        analysis["clinical_significance"] = f"Analysis suggests the following conditions: {', '.join(analysis['potential_conditions'])}. Clinical correlation recommended."
    else:
        analysis["clinical_significance"] = "No significant abnormalities detected in the provided text. Routine follow-up recommended."
    
    # Generate recommendations
    if "diabetes" in str(analysis["potential_conditions"]).lower():
        analysis["recommendations"].extend([
            "Schedule follow-up with primary care physician",
            "Consider diabetes education program",
            "Monitor blood glucose regularly",
            "Dietary modification - reduce refined carbohydrates"
        ])
    
    if "hypertension" in str(analysis["potential_conditions"]).lower():
        analysis["recommendations"].extend([
            "Home blood pressure monitoring",
            "DASH diet implementation",
            "Sodium restriction",
            "Regular cardiovascular exercise"
        ])
    
    if "cholesterol" in str(analysis["potential_conditions"]).lower():
        analysis["recommendations"].extend([
            "Lipid panel recheck in 3 months",
            "Heart-healthy diet (Mediterranean pattern)",
            "Consider statin therapy based on risk factors"
        ])
    
    if not analysis["recommendations"]:
        analysis["recommendations"] = [
            "Continue routine health maintenance",
            "Schedule regular check-ups",
            "Maintain healthy lifestyle"
        ]
    
    return analysis
