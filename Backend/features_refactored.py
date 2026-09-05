"""
Refactored Feature Engineering Module
Integrates all sub-modules for cleaner code organization
"""

from validators import InputValidator
from text_processor import TextProcessor
from predictor import ModelPredictor, OverrideEngine
from response_builder import ResponseBuilder


class FeatureProcessor:
    """Main feature processing orchestrator (simplified)"""
    
    def __init__(self, trusted_sources, suspicious_sources, sensational_keywords):
        self.text_processor = TextProcessor(trusted_sources, suspicious_sources, sensational_keywords)
        self.input_validator = InputValidator()
    
    def clean_text(self, text):
        """Delegate to text processor"""
        return self.text_processor.clean_text(text)
    
    def validate_input_quality(self, text, vectorized_features):
        """Delegate to input validator"""
        return self.input_validator.validate(text, vectorized_features)
    
    def get_source_credibility(self, source):
        """Delegate to text processor"""
        return self.text_processor.get_source_credibility(source)
    
    def extract_sensationalism_score(self, text):
        """Delegate to text processor"""
        return self.text_processor.extract_sensationalism_score(text)
    
    def check_implausible_claims(self, text):
        """Delegate to text processor"""
        return self.text_processor.check_implausible_claims(text)
    
    def create_enhanced_features(self, statement, web, category):
        """Delegate to text processor"""
        return self.text_processor.create_enhanced_features(statement, web, category)


class PredictionEngine:
    """Main prediction orchestrator (simplified)"""
    
    def __init__(self, models, feature_processor):
        self.vectorizer = models['vectorizer']
        self.feature_processor = feature_processor
        self.model_predictor = ModelPredictor(models['svc'], models['lr'], models['gb'])
        self.override_engine = OverrideEngine()
    
    def predict(self, text, web, category):
        """Main prediction pipeline"""
        # STEP 1: Vectorize
        input_features = self.feature_processor.create_enhanced_features(text, web, category)
        vectorized_text = self.vectorizer.transform([input_features])
        
        # STEP 2: Validate input
        is_valid, quality_score, validation_reason = \
            self.feature_processor.validate_input_quality(text, vectorized_text)
        
        if not is_valid:
            return ResponseBuilder.build_indeterminate_response(
                quality_score, validation_reason, len(text)
            )
        
        # STEP 3: Extract features
        credibility = self.feature_processor.get_source_credibility(web)
        sensationalism = self.feature_processor.extract_sensationalism_score(text)
        implausible = self.feature_processor.check_implausible_claims(text)
        
        # STEP 4: Get model predictions
        predictions = self.model_predictor.predict(vectorized_text)
        
        # STEP 5: Ensemble voting
        ensemble_result = self.model_predictor.ensemble_vote(
            predictions['predictions'], 
            predictions['scores'],
            quality_score
        )
        
        # STEP 6: Apply overrides
        override_result = self.override_engine.apply(
            ensemble_result['prediction'],
            ensemble_result['confidence'],
            web, category, sensationalism, implausible
        )
        
        # STEP 7: Build response
        return ResponseBuilder.build_normal_response(
            override_result['prediction'],
            override_result['confidence'],
            predictions['votes'],
            ensemble_result['agreement'],
            credibility,
            sensationalism,
            implausible,
            override_result,
            quality_score,
            web,
            category,
            len(text),
            ensemble_result['decision_score']
        )