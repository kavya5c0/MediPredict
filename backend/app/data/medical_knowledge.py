"""
Real Medical Knowledge Base
Sources: WHO, CDC, Mayo Clinic, NIH, American Heart Association
"""

MEDICAL_KNOWLEDGE_BASE = {
    "diabetes": {
        "symptoms": [
            "Increased thirst and urination",
            "Extreme hunger",
            "Unexplained weight loss",
            "Fatigue and irritability",
            "Blurred vision",
            "Slow-healing sores",
            "Frequent infections (gums, skin, vaginal)",
            "Tingling or numbness in hands or feet"
        ],
        "risk_factors": [
            "Overweight or obesity",
            "Inactivity (less than 150 minutes/week of exercise)",
            "Family history of type 2 diabetes",
            "Age 45 or older",
            "Prediabetes",
            "Gestational diabetes",
            "Polycystic ovary syndrome",
            "High blood pressure",
            "Abnormal cholesterol levels"
        ],
        "prevention": [
            "Maintain healthy weight",
            "Get at least 150 minutes of moderate aerobic activity weekly",
            "Avoid tobacco use",
            "Eat a healthy diet rich in fruits, vegetables, and whole grains",
            "Limit sugary beverages and refined carbohydrates",
            "Control blood pressure and cholesterol"
        ],
        "treatment": [
            "Blood sugar monitoring (A1C tests)",
            "Oral medications (metformin, sulfonylureas, etc.)",
            "Insulin therapy (for type 1 or advanced type 2)",
            "Medical nutrition therapy",
            "Physical activity",
            "Continuous glucose monitoring"
        ],
        "complications": [
            "Cardiovascular disease (heart attack, stroke)",
            "Kidney disease (nephropathy)",
            "Eye damage (retinopathy)",
            "Nerve damage (neuropathy)",
            "Foot damage (ulcers, amputation)",
            "Skin conditions",
            "Hearing impairment"
        ]
    },
    "hypertension": {
        "symptoms": [
            "Headaches (especially in the morning)",
            "Nosebleeds",
            "Shortness of breath",
            "Dizziness",
            "Chest pain",
            "Vision changes",
            "Blood in urine"
        ],
        "risk_factors": [
            "Age (risk increases with age)",
            "Race (higher in African Americans)",
            "Family history",
            "Being overweight or obese",
            "Not being physically active",
            "Too much sodium in diet",
            "Drinking too much alcohol",
            "Stress"
        ],
        "prevention": [
            "DASH diet (Dietary Approaches to Stop Hypertension)",
            "Limit sodium to less than 2,300 mg/day",
            "Maintain healthy weight",
            "Regular physical activity (150 minutes/week)",
            "Limit alcohol (no more than 2 drinks/day for men, 1 for women)",
            "Manage stress through relaxation techniques",
            "Quit smoking"
        ],
        "treatment": [
            "Lifestyle modifications (diet, exercise, weight loss)",
            "ACE inhibitors (lisinopril, enalapril)",
            "ARBs (losartan, valsartan)",
            "Calcium channel blockers (amlodipine, diltiazem)",
            "Diuretics (hydrochlorothiazide, furosemide)",
            "Beta blockers (metoprolol, atenolol)"
        ],
        "target_blood_pressure": [
            "Normal: Less than 120/80 mmHg",
            "Elevated: 120-129/<80 mmHg",
            "Stage 1: 130-139/80-89 mmHg",
            "Stage 2: 140+/90+ mmHg",
            "Hypertensive crisis: >180/120 mmHg"
        ]
    },
    "heart_disease": {
        "symptoms": [
            "Chest pain or discomfort (angina)",
            "Shortness of breath",
            "Pain in neck, jaw, throat, upper abdomen or back",
            "Pain, numbness, weakness or coldness in legs or arms",
            "Heart palpitations",
            "Fatigue",
            "Swelling in legs, ankles and feet",
            "Dizziness"
        ],
        "risk_factors": [
            "High blood pressure",
            "High cholesterol",
            "Smoking",
            "Diabetes",
            "Overweight or obesity",
            "Physical inactivity",
            "Unhealthy diet",
            "Excessive alcohol",
            "Family history",
            "Age (risk increases with age)",
            "Stress"
        ],
        "prevention": [
            "Quit smoking",
            "Control blood pressure",
            "Manage cholesterol",
            "Maintain healthy weight",
            "Exercise regularly (150 minutes/week)",
            "Eat a heart-healthy diet (low saturated fat, trans fat, sodium)",
            "Limit alcohol",
            "Manage stress",
            "Get adequate sleep (7-9 hours)"
        ],
        "treatment": [
            "Lifestyle changes",
            "Medications (statins, beta blockers, ACE inhibitors)",
            "Medical procedures (angioplasty, bypass surgery)",
            "Cardiac rehabilitation",
            "Implantable devices (pacemakers, defibrillators)"
        ],
        "diet_recommendations": [
            "Eat more: fruits, vegetables, whole grains, lean proteins",
            "Eat less: saturated fats, trans fats, sodium, added sugars",
            "Follow Mediterranean diet or DASH diet",
            "Choose healthy fats (olive oil, avocado, nuts)",
            "Limit red meat to once or twice a week",
            "Eat fish twice a week (salmon, tuna, mackerel)"
        ]
    },
    "general_health": {
        "nutrition": {
            "fruits_vegetables": "5-9 servings daily",
            "whole_grains": "3-6 servings daily",
            "protein": "Lean meats, poultry, fish, beans, nuts",
            "fats": "Limit saturated and trans fats",
            "sugar": "Less than 10% of daily calories",
            "sodium": "Less than 2,300 mg/day"
        },
        "exercise": {
            "adults": "150 minutes moderate or 75 minutes vigorous weekly",
            "muscle_strengthening": "2+ days per week",
            "children": "60 minutes daily",
            "types": ["aerobic", "strength training", "flexibility", "balance"]
        },
        "sleep": {
            "adults": "7-9 hours per night",
            "teenagers": "8-10 hours per night",
            "children": "9-12 hours per night",
            "quality": "Consistent schedule, dark room, no screens before bed"
        },
        "hydration": {
            "daily_intake": "8 glasses (64 oz) for adults",
            "sources": "Water, herbal tea, fruits, vegetables",
            "avoid": "Excessive caffeine, sugary drinks"
        }
    },
    "lab_values": {
        "blood_glucose": {
            "normal_fasting": "70-99 mg/dL",
            "normal_postprandial": "Less than 140 mg/dL",
            "prediabetes_fasting": "100-125 mg/dL",
            "diabetes_fasting": "126 mg/dL or higher",
            "a1c_normal": "Below 5.7%",
            "a1c_prediabetes": "5.7-6.4%",
            "a1c_diabetes": "6.5% or higher"
        },
        "cholesterol": {
            "total_cholesterol": {
                "desirable": "Less than 200 mg/dL",
                "borderline_high": "200-239 mg/dL",
                "high": "240 mg/dL or higher"
            },
            "ldl_bad": {
                "optimal": "Less than 100 mg/dL",
                "near_optimal": "100-129 mg/dL",
                "borderline_high": "130-159 mg/dL",
                "high": "160-189 mg/dL",
                "very_high": "190 mg/dL or higher"
            },
            "hdl_good": {
                "men": "40 mg/dL or higher",
                "women": "50 mg/dL or higher"
            },
            "triglycerides": {
                "normal": "Less than 150 mg/dL",
                "borderline_high": "150-199 mg/dL",
                "high": "200-499 mg/dL",
                "very_high": "500 mg/dL or higher"
            }
        },
        "blood_pressure": {
            "normal": "Less than 120/80 mmHg",
            "elevated": "120-129/<80 mmHg",
            "stage_1": "130-139/80-89 mmHg",
            "stage_2": "140+/90+ mmHg",
            "hypertensive_crisis": ">180/120 mmHg"
        }
    }
}

DISEASE_RISK_CALCULATORS = {
    "diabetes": {
        "bmi": {
            "low_risk": "< 25",
            "moderate_risk": "25-29.9",
            "high_risk": "30+"
        },
        "age": {
            "low_risk": "< 45",
            "moderate_risk": "45-64",
            "high_risk": "65+"
        },
        "waist_circumference": {
            "men": {
                "low_risk": "< 40 inches",
                "high_risk": "40+ inches"
            },
            "women": {
                "low_risk": "< 35 inches",
                "high_risk": "35+ inches"
            }
        }
    },
    "cardiovascular": {
        "bmi": {
            "low_risk": "< 25",
            "moderate_risk": "25-29.9",
            "high_risk": "30+"
        },
        "cholesterol": {
            "total": {
                "optimal": "< 200",
                "borderline": "200-239",
                "high": "240+"
            },
            "ldl": {
                "optimal": "< 100",
                "near_optimal": "100-129",
                "borderline": "130-159",
                "high": "160+"
            }
        },
        "blood_pressure": {
            "optimal": "< 120/80",
            "elevated": "120-129/< 80",
            "stage_1": "130-139/80-89",
            "stage_2": "140+/90+"
        }
    }
}

HEALTH_SCREENING_RECOMMENDATIONS = {
    "age_18_39": [
        "Blood pressure check every 2 years",
        "Cholesterol check every 5 years",
        "BMI check annually",
        "Blood glucose every 3 years if overweight",
        "Skin cancer exam",
        "Cervical cancer screening (women)",
        "Testicular cancer screening (men)"
    ],
    "age_40_49": [
        "Blood pressure check annually",
        "Cholesterol check every 5 years",
        "Diabetes screening every 3 years",
        "Mammogram every 1-2 years (women)",
        "Colon cancer screening starting at 45",
        "Prostate cancer screening (men)",
        "Eye exam every 2-4 years"
    ],
    "age_50_64": [
        "Blood pressure check annually",
        "Cholesterol check every 1-2 years",
        "Diabetes screening every 3 years",
        "Mammogram every 1-2 years (women)",
        "Colon cancer screening every 10 years",
        "Bone density scan (women)",
        "Lung cancer screening if smoker",
        "Shingles vaccine"
    ],
    "age_65_plus": [
        "Blood pressure check annually",
        "Cholesterol check annually",
        "Diabetes screening every 3 years",
        "Mammogram every 1-2 years (women)",
        "Colon cancer screening every 10 years",
        "Bone density scan (women)",
        "Annual flu vaccine",
        "Pneumococcal vaccine",
        "Shingles vaccine",
        "Hearing test"
    ]
}
