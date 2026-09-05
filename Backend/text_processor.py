"""
Text Processing Module
Handles text cleaning, source credibility, sensationalism, and feature creation
"""

import re
import string


class TextProcessor:
    """Processes text for fake news detection"""
    
    def __init__(self, trusted_sources, suspicious_sources, sensational_keywords):
        self.trusted_sources = [s.lower() for s in trusted_sources]
        self.suspicious_sources = [s.lower() for s in suspicious_sources]
        self.sensational_keywords = [k.lower() for k in sensational_keywords]
        
        # Emergency/disaster words that are REAL news, not sensational
        self.emergency_words = [
            'fire', 'outage', 'blackout', 'power cut', 'accident', 
            'collapsed', 'flooding', 'earthquake', 'storm', 'hospital',
            'casualties', 'injured', 'evacuated', 'rescue', 'blaze'
        ]
        
        # Truly sensational/manipulative words
        self.fake_sensational = [
            'shocking', 'unbelievable', 'mind blowing', 'you won\'t believe',
            'doctors hate', 'this one trick', 'government hiding', 
            'they don\'t want', 'secret', 'conspiracy', 'cover up',
            'omg', 'wtf', 'breaking', 'urgent', 'alert'
        ]
    
    def clean_text(self, text):
        """
        FIXED: Minimal preprocessing to match training pipeline.
        
        The models were trained with TF-IDF using stop_words='english'.
        No aggressive cleaning was applied to training data, so we shouldn't
        apply it to prediction data either.
        
        Only do:
        - Normalize whitespace
        - Lowercase (TF-IDF does this)
        """
        if not text:
            return ""
        
        text = str(text).strip()
        
        # Only normalize whitespace - don't remove URLs or content
        text = ' '.join(text.split())
        
        # Lowercase for consistency (TF-IDF requires this)
        text = text.lower()
        
        return text
    
    def get_source_credibility(self, source):
        """Score source credibility: 0-100"""
        if not source:
            return 50  # Neutral for unknown sources
        
        source_lower = source.lower().strip()
        
        # Trusted sources
        for trusted in self.trusted_sources:
            if trusted in source_lower:
                return 90
        
        # Suspicious sources
        for suspicious in self.suspicious_sources:
            if suspicious in source_lower:
                return 20
        
        # Social media platforms - slightly suspicious but not auto-fake
        social_platforms = ['whatsapp', 'facebook', 'twitter', 'telegram', 'instagram']
        if any(platform in source_lower for platform in social_platforms):
            return 40
        
        return 60  # Default slightly positive
    
    def extract_sensationalism_score(self, text):
        """
        FIXED: Score 0-10. 
        Real emergency news gets LOWER scores.
        Manipulative language gets HIGHER scores.
        """
        if not text:
            return 0
        
        text_lower = text.lower()
        score = 0
        
        # Check for fake sensational words (+2 each)
        for word in self.fake_sensational:
            if word in text_lower:
                score += 2
        
        # Check for ALL CAPS words (shouting)
        words = text.split()
        caps_count = sum(1 for w in words if w.isupper() and len(w) > 2)
        score += min(caps_count * 0.5, 3)
        
        # Check for excessive exclamation marks
        excl_count = text.count('!')
        score += min(excl_count * 0.5, 2)
        
        # Check for excessive question marks
        ques_count = text.count('?')
        score += min(ques_count * 0.3, 1.5)
        
        # PENALTY REDUCTION for real emergency context
        # If text contains emergency words in a factual structure, reduce score
        emergency_matches = sum(1 for word in self.emergency_words if word in text_lower)
        if emergency_matches > 0:
            # This looks like real news, reduce sensationalism score
            score = max(0, score - 2)
        
        # PENALTY REDUCTION for trusted source indicators in text
        factual_patterns = ['reported', 'officials said', 'according to', 'sources confirmed']
        for pattern in factual_patterns:
            if pattern in text_lower:
                score = max(0, score - 1)
                break
        
        return min(score, 10)
    
    def check_implausible_claims(self, text):
        """
        FIXED: Only flag physically/scientifically impossible claims.
        Real emergency/disaster news is NEVER flagged.
        """
        if not text:
            return False
        
        text_lower = text.lower().strip()
        
        # === WHITELIST: Real emergency/disaster news ===
        real_emergency_patterns = [
            'fire reported', 'power outage', 'blackout', 'power cut',
            'fire at', 'fire broke out', 'caught fire', 'blaze at',
            'outage in', 'electricity cut', 'grid failure', 'substation',
            'hospital fire', 'building fire', 'factory fire', 'residential fire',
            'accident', 'collapsed', 'flooding', 'earthquake', 'storm damage',
            'train accident', 'bus accident', 'car crash', 'bridge collapsed'
        ]
        
        for pattern in real_emergency_patterns:
            if pattern in text_lower:
                return False  # This is real news, NOT implausible
        
        # === BLACKLIST: Truly impossible/absurd claims ===
        impossible_patterns = [
            'cures all diseases', 'cures cancer', '100% effective cure',
            'never get sick again', 'aliens landed', 'aliens found',
            'ufo confirmed', 'perpetual motion', 'defies physics',
            'defies gravity', '5g causes covid', '5g spreads coronavirus',
            'vaccine causes autism', 'vaccine contains microchip',
            'magnetic vaccine', 'bill gates tracking', 'population control',
            'depopulation agenda', 'drinking bleach cures', 'drinking urine cures',
            'cow urine cures', 'one weird trick', 'doctors hate this',
            'big pharma doesn\'t want', 'they don\'t want you to know',
            'secret cure', 'miracle cure', 'instant weight loss',
            'lose 10kg in 1 day', 'government confirms conspiracy'
        ]
        
        for pattern in impossible_patterns:
            if pattern in text_lower:
                return True  # Actually implausible
        
        return False
    
    def create_enhanced_features(self, statement, web, category):
        """
        CRITICAL FIX: Use only the statement, no augmentation.
        
        The models were trained on raw 'Statement' text from IFND dataset.
        Modifying/repeating/augmenting the text creates different TF-IDF 
        vectors that the models never saw, causing poor predictions.
        
        Solution: Return statement with minimal preprocessing only.
        """
        # Return statement as-is with only basic cleanup
        # This matches what the training data looked like
        return statement.strip() if statement else ""