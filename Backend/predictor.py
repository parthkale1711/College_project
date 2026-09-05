"""
Prediction Module
Handles model predictions, ensemble voting, and overrides
"""

import numpy as np


class ModelPredictor:
    """Runs predictions using ensemble of models"""
    
    def __init__(self, svc_model, lr_model, gb_model):
        self.svc_model = svc_model
        self.lr_model = lr_model
        self.gb_model = gb_model
    
    def predict(self, vectorized_text):
        """Get predictions from all 3 models"""
        svc_pred = self.svc_model.predict(vectorized_text)[0]
        lr_pred = self.lr_model.predict(vectorized_text)[0]
        gb_pred = self.gb_model.predict(vectorized_text)[0]
        
        svc_score = self._get_svc_score(vectorized_text)
        lr_score = self._get_lr_score(vectorized_text)
        gb_score = self._get_gb_score(vectorized_text)
        
        return {
            'predictions': [svc_pred, lr_pred, gb_pred],
            'scores': [svc_score, lr_score, gb_score],
            'votes': {
                'LinearSVC': 'Fake' if svc_pred == 1 else 'Real',
                'Logistic Regression': 'Fake' if lr_pred == 1 else 'Real',
                'Gradient Boosting': 'Fake' if gb_pred == 1 else 'Real'
            }
        }
    
    def _get_svc_score(self, vectorized_text):
        try:
            return abs(self.svc_model.decision_function(vectorized_text)[0])
        except:
            return 1.0
    
    def _get_lr_score(self, vectorized_text):
        try:
            return abs(self.lr_model.decision_function(vectorized_text)[0])
        except:
            return 1.0
    
    def _get_gb_score(self, vectorized_text):
        try:
            gb_proba = self.gb_model.predict_proba(vectorized_text)[0]
            return max(gb_proba)
        except:
            return 1.0
    
    def ensemble_vote(self, predictions, scores, quality_score):
        """Calculate ensemble prediction and confidence"""
        final_prediction = int(np.round(np.mean(predictions)))
        
        agreement = sum(predictions) / len(predictions)
        confidence_ratio = max(agreement, 1 - agreement)
        
        avg_decision_score = sum(scores) / len(scores)
        combined_confidence = (confidence_ratio * 0.6) + (min(avg_decision_score / 2, 1.0) * 0.4)
        
        # FIXED: Less aggressive quality penalty
        combined_confidence = combined_confidence * (0.9 + quality_score * 0.1)
        confidence_percentage = int(combined_confidence * 100)
        
        return {
            'prediction': final_prediction,
            'confidence': confidence_percentage,
            'agreement': f"{int(confidence_ratio * 100)}%",
            'decision_score': float(avg_decision_score)
        }


class OverrideEngine:
    """Applies smart override rules - CONSERVATIVE"""
    
    def apply(self, prediction, confidence, web, category, sensationalism, implausible):
        """Apply override logic - ONLY for extreme cases"""
        
        # OVERRIDE 1: Only flip if models are uncertain AND truly impossible
        if implausible and prediction == 0 and confidence < 45:
            return {
                'prediction': 1,
                'confidence': 50,
                'applied': True,
                'reason': "Highly implausible claim with very low confidence"
            }
        
        # OVERRIDE 2: Multi-flag - requires 4+ flags AND very low confidence
        suspicious_sources = ['whatsapp', 'facebook', 'twitter', 'viral', 'forward']
        sensitive_topics = ['COVID-19', 'HEALTH']
        
        red_flags = self._count_red_flags(web, category, sensationalism, implausible,
                                          suspicious_sources, sensitive_topics)
        
        if red_flags['count'] >= 4 and prediction == 0 and confidence < 35:
            return {
                'prediction': 1,
                'confidence': max(45, confidence),
                'applied': True,
                'reason': f"Severe risk indicators: {', '.join(red_flags['list'])}"
            }
        
        # No override
        return {
            'prediction': prediction,
            'confidence': confidence,
            'applied': False,
            'reason': None
        }
    
    def _count_red_flags(self, web, category, sensationalism, implausible,
                        suspicious_sources, sensitive_topics):
        count = 0
        flags_list = []
        
        if any(sus in web.lower() for sus in suspicious_sources):
            count += 1
            flags_list.append(f"Unverified source ({web})")
        
        if category.upper() in sensitive_topics:
            count += 0.5
            flags_list.append(f"Sensitive topic ({category})")
        
        if sensationalism > 7:
            count += 1
            flags_list.append(f"High sensationalism ({sensationalism:.1f}/10)")
        
        if implausible:
            count += 1
            flags_list.append("Implausible claims")
        
        return {'count': count, 'list': flags_list}