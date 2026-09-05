"""
Configuration and Model Loading Module
Handles all model loading and constant definitions
"""

import joblib

class ModelLoader:
    """Singleton class to load and store all models"""
    
    def __init__(self):
        self.svc_model = None
        self.lr_model = None
        self.gb_model = None
        self.vectorizer = None
        self.metadata = None
        self.INDIAN_TRUSTED_SOURCES = []
        self.SUSPICIOUS_SOURCES = []
        self.INDIAN_SENSATIONAL_KEYWORDS = {}
        
    def load_models(self):
        """Load all models and metadata"""
        print("Loading models for Indian Fake News Detection...")
        try:
            self.svc_model = joblib.load('fake_news_svc.pkl')
            self.lr_model = joblib.load('fake_news_lr.pkl')
            self.gb_model = joblib.load('fake_news_gb.pkl')
            self.vectorizer = joblib.load('tfidf_vectorizer_v2.pkl')
            self.metadata = joblib.load('indian_context_metadata.pkl')
            
            self.INDIAN_TRUSTED_SOURCES = self.metadata['trusted_sources']
            self.SUSPICIOUS_SOURCES = self.metadata['suspicious_sources']
            self.INDIAN_SENSATIONAL_KEYWORDS = self.metadata['sensational_keywords']
            
            print("✅ All models and metadata loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise
    
    def get_models(self):
        """Return all models as a dictionary"""
        return {
            'svc': self.svc_model,
            'lr': self.lr_model,
            'gb': self.gb_model,
            'vectorizer': self.vectorizer,
            'trusted_sources': self.INDIAN_TRUSTED_SOURCES,
            'suspicious_sources': self.SUSPICIOUS_SOURCES,
            'sensational_keywords': self.INDIAN_SENSATIONAL_KEYWORDS
        }

# Global instance
model_loader = ModelLoader()