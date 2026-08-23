import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import pandas as pd

class HealthRecommendationEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.user_profiles = {}
        self.health_tips = self._load_health_tips()
        
    def _load_health_tips(self) -> List[Dict]:
        """Load predefined health tips and recommendations"""
        return [
            {
                "category": "diet",
                "tip": "Include more fruits and vegetables in your diet",
                "condition": "general"
            },
            {
                "category": "exercise",
                "tip": "Aim for at least 150 minutes of moderate exercise per week",
                "condition": "general"
            },
            {
                "category": "sleep",
                "tip": "Maintain 7-9 hours of quality sleep each night",
                "condition": "general"
            },
            {
                "category": "hydration",
                "tip": "Drink at least 8 glasses of water daily",
                "condition": "general"
            },
            {
                "category": "stress",
                "tip": "Practice stress reduction techniques like meditation",
                "condition": "general"
            },
            {
                "category": "diet",
                "tip": "Limit processed foods and added sugars",
                "condition": "diabetes"
            },
            {
                "category": "exercise",
                "tip": "Low-impact exercises like swimming are recommended",
                "condition": "arthritis"
            },
            {
                "category": "diet",
                "tip": "Follow a low-sodium diet to manage blood pressure",
                "condition": "hypertension"
            },
            {
                "category": "exercise",
                "tip": "Cardio exercises can improve heart health",
                "condition": "heart_disease"
            },
            {
                "category": "respiratory",
                "tip": "Avoid triggers that cause respiratory distress",
                "condition": "asthma"
            }
        ]
    
    def create_user_profile(self, user_id: str, health_data: Dict):
        """Create or update user health profile"""
        profile = {
            "age": health_data.get("age", 0),
            "gender": health_data.get("gender", ""),
            "conditions": health_data.get("conditions", []),
            "medications": health_data.get("medications", []),
            "lifestyle": health_data.get("lifestyle", {}),
            "preferences": health_data.get("preferences", {})
        }
        
        self.user_profiles[user_id] = profile
        return profile
    
    def get_personalized_recommendations(self, user_id: str) -> List[Dict]:
        """Generate personalized health recommendations"""
        if user_id not in self.user_profiles:
            return self._get_general_recommendations()
        
        profile = self.user_profiles[user_id]
        recommendations = []
        
        # Condition-specific recommendations
        for condition in profile["conditions"]:
            condition_lower = condition.lower().replace(" ", "_")
            for tip in self.health_tips:
                if tip["condition"] == condition_lower:
                    recommendations.append({
                        "category": tip["category"],
                        "recommendation": tip["tip"],
                        "priority": "high",
                        "reason": f"Based on your condition: {condition}"
                    })
        
        # Age-specific recommendations
        if profile["age"] > 50:
            recommendations.append({
                "category": "screening",
                "recommendation": "Schedule regular cancer screenings",
                "priority": "medium",
                "reason": "Age-based recommendation"
            })
        
        # Lifestyle-based recommendations
        if profile["lifestyle"].get("smoking", False):
            recommendations.append({
                "category": "lifestyle",
                "recommendation": "Consider smoking cessation programs",
                "priority": "high",
                "reason": "Smoking health risk"
            })
        
        if profile["lifestyle"].get("activity_level", "moderate") == "sedentary":
            recommendations.append({
                "category": "exercise",
                "recommendation": "Start with light exercises and gradually increase",
                "priority": "medium",
                "reason": "Sedentary lifestyle detected"
            })
        
        # Add general recommendations if few specific ones
        if len(recommendations) < 3:
            recommendations.extend(self._get_general_recommendations()[:3])
        
        return recommendations[:10]  # Limit to top 10
    
    def _get_general_recommendations(self) -> List[Dict]:
        """Get general health recommendations"""
        general_tips = [tip for tip in self.health_tips if tip["condition"] == "general"]
        
        return [
            {
                "category": tip["category"],
                "recommendation": tip["tip"],
                "priority": "low",
                "reason": "General health advice"
            }
            for tip in general_tips
        ]
    
    def find_similar_users(self, user_id: str, n_neighbors: int = 5) -> List[str]:
        """Find users with similar health profiles"""
        if user_id not in self.user_profiles:
            return []
        
        # Create feature vectors from user profiles
        profiles = list(self.user_profiles.values())
        profile_texts = []
        
        for profile in profiles:
            text = f"{profile['age']} {profile['gender']} {' '.join(profile['conditions'])}"
            text += f" {' '.join(profile['medications'])}"
            profile_texts.append(text)
        
        # Vectorize and compute similarities
        tfidf_matrix = self.vectorizer.fit_transform(profile_texts)
        similarities = cosine_similarity(tfidf_matrix)
        
        user_index = list(self.user_profiles.keys()).index(user_id)
        similar_indices = np.argsort(similarities[user_index])[::-1][1:n_neighbors+1]
        
        similar_users = [list(self.user_profiles.keys())[i] for i in similar_indices]
        return similar_users
    
    def cluster_users(self, n_clusters: int = 3) -> Dict:
        """Cluster users based on health profiles"""
        if len(self.user_profiles) < n_clusters:
            return {"error": "Not enough users for clustering"}
        
        # Create feature matrix
        profile_texts = []
        for profile in self.user_profiles.values():
            text = f"{profile['age']} {profile['gender']} {' '.join(profile['conditions'])}"
            text += f" {' '.join(profile['medications'])}"
            profile_texts.append(text)
        
        tfidf_matrix = self.vectorizer.fit_transform(profile_texts)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(tfidf_matrix.toarray())
        
        # Assign users to clusters
        cluster_assignments = {}
        for user_id, cluster in zip(self.user_profiles.keys(), clusters):
            cluster_assignments[user_id] = int(cluster)
        
        return {
            "clusters": cluster_assignments,
            "cluster_centers": kmeans.cluster_centers_.tolist()
        }
