"""
Input Validation Module - FINAL FIXED VERSION
Handles news headlines properly, rejects gibberish
"""

import re
import numpy as np
from collections import Counter
from scipy.sparse import issparse


class InputValidator:
    """Validates input quality - understands news headline structure"""
    
    def __init__(self):
        self.common_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 
            'for', 'of', 'said', 'says', 'news', 'new', 'will', 'has', 'have', 'been',
            'this', 'that', 'with', 'from', 'but', 'not', 'can', 'their', 'which',
            'india', 'indian', 'delhi', 'mumbai', 'government', 'minister', 'prime',
            'modi', 'people', 'country', 'state', 'party', 'court', 'police',
            'report', 'according', 'official', 'statement', 'announced', 'confirmed',
            'fire', 'power', 'outage', 'hospital', 'reported', 'accident', 'collapsed',
            'storm', 'earthquake', 'flooding', 'blaze', 'casualties', 'injured',
            'metro', 'airport', 'city', 'corridor', 'launches', 'launch', 'connecting',
            'train', 'bus', 'road', 'bridge', 'highway', 'station'
        }
        
        # Headlines often skip articles/subjects - these are VALID headline patterns
        self.headline_patterns = [
            # Noun + Verb: "Delhi Metro launches...", "PM Modi announces..."
            r'\b[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+\s+(launches?|announces?|confirms?|reports?|approves?|declares?|starts?|begins?|opens?|closes?|wins?|loses?|dies?|killed|injured)\b',
            # Location + Event: "Mumbai fire reported...", "Delhi rains continue..."
            r'\b[A-Z][a-zA-Z]+\s+(fire|outage|rains?|floods?|earthquake|storm|accident|blast|attack|crash)\b',
            # Organization + Action: "ISRO launches...", "RBI keeps..."
            r'\b[A-Z]{2,}\s+(launches?|keeps?|holds?|maintains?|issues?|releases?|signs?|approves?)\b',
            # Number + People + Action: "16 killed in...", "5 injured..."
            r'\b\d+\s+(people|persons|deaths?|injured|killed|missing|rescued)\b',
            # Person + Verb: "Modi says...", "Rahul claims..."
            r'\b[A-Z][a-zA-Z]+\s+(says|said|claims?|states?|adds?|denies?|accepts?)\b',
            # Government/Official + Action
            r'\b(government|court|police|army|ministry|cabinet)\s+(announces?|approves?|rejects?|orders?|directs?)\b',
        ]
        
        # Proper noun indicators (capitalized words that look like real names/places)
        self.proper_noun_pattern = r'\b[A-Z][a-zA-Z]{2,}\b'
        
        # STRONG action words (verbs that indicate real news, not random words)
        self.strong_action_words = {
            'launches', 'announces', 'confirms', 'reports', 'approves', 
            'declares', 'starts', 'begins', 'opens', 'closes', 'wins', 'loses',
            'said', 'claims', 'states', 'adds', 'denies', 'accepts',
            'connecting', 'linking', 'building', 'constructing', 'inaugurates'
        }
        
        # WEAK action words - alone they don't prove it's news
        self.weak_action_words = {
            'died', 'killed', 'injured', 'dead'
        }
        
        # Gibberish indicators
        self.gibberish_bigrams = [
            'random names', 'names died', 'someone random', 'qwerty asdf',
            'asdf ghjk', 'zxcvbnm qwerty', 'lorem ipsum'
        ]
    
    def validate(self, text, vectorized_features):
        if not text or text.strip() == "":
            return False, 0.05, "Empty input provided"
        
        clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = clean_text.split()
        original_text = text.strip()
        
        # Run all checks
        checks = [
            self._check_length(words),
            self._check_alphabetic_ratio(original_text),
            self._check_repetition(original_text),
            self._check_vowel_pattern(words),
            self._check_tfidf_sparsity(vectorized_features),
            self._check_word_length(words),
            self._check_common_words(words),
            self._check_headline_structure(original_text),
            self._check_gibberish_patterns(original_text)
        ]
        
        for is_valid, score, reason in checks:
            if not is_valid:
                return False, score, reason
        
        quality_score = self._calculate_quality_score(original_text, words, vectorized_features)
        
        if quality_score < 0.12:
            return False, quality_score, "Overall input quality too low"
        
        return True, quality_score, "Input quality acceptable"
    
    def _check_length(self, words):
        if len(words) < 2:
            return False, 0.15, "Input too short (minimum 2 words)"
        return True, 1.0, None
    
    def _check_alphabetic_ratio(self, text):
        valid_chars = sum(c.isalpha() or c.isdigit() or c.isspace() or c in ',.:-' for c in text)
        total_chars = len(text)
        if total_chars > 0:
            valid_ratio = valid_chars / total_chars
            if valid_ratio < 0.5:
                return False, 0.12, "Too many special characters"
        return True, 1.0, None
    
    def _check_repetition(self, text):
        text_no_spaces = text.replace(" ", "")
        if text_no_spaces:
            char_counts = Counter(text_no_spaces)
            max_char_freq = max(char_counts.values())
            if max_char_freq > len(text_no_spaces) * 0.35:
                return False, 0.10, "Excessive character repetition"
        return True, 1.0, None
    
    def _check_vowel_pattern(self, words):
        vowels = set('aeiou')
        words_with_vowels = sum(1 for word in words if any(c in vowels for c in word.lower()))
        vowel_ratio = words_with_vowels / len(words) if words else 0
        if len(words) > 3 and vowel_ratio < 0.25:
            return False, 0.14, "Unnatural word patterns"
        return True, 1.0, None
    
    def _check_tfidf_sparsity(self, vectorized_features):
        if issparse(vectorized_features):
            non_zero_features = vectorized_features.nnz
            total_features = vectorized_features.shape[1]
        else:
            non_zero_features = np.count_nonzero(vectorized_features)
            total_features = vectorized_features.shape[1]
        feature_density = non_zero_features / total_features if total_features > 0 else 0
        if feature_density < 0.0001:
            return False, 0.08, "No recognizable words found in vocabulary"
        return True, 1.0, None
    
    def _check_word_length(self, words):
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        if avg_word_length < 2.0 or avg_word_length > 20:
            return False, 0.11, "Unusual word length pattern"
        return True, 1.0, None
    
    def _check_common_words(self, words):
        words_lower = set(word.lower() for word in words)
        common_found = len(words_lower.intersection(self.common_words))
        if len(words) >= 5 and common_found == 0:
            return False, 0.16, "No common words found"
        return True, 1.0, None
    
    def _check_headline_structure(self, text):
        """
        News headlines don't need full sentences.
        They need: proper nouns + strong action words, or recognizable news structure.
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        # Check 1: Does it match known headline patterns?
        for pattern in self.headline_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True, 1.0, None
        
        # Check 2: Does it have proper nouns? (Capitalized words = real names/places)
        proper_nouns = re.findall(self.proper_noun_pattern, text)
        has_proper_nouns = len(proper_nouns) >= 1
        
        # Check 3: Does it have STRONG action/verb words?
        has_strong_action = any(w in self.strong_action_words for w in words)
        
        # Check 4: Does it have WEAK action words? (needs more context)
        has_weak_action = any(w in self.weak_action_words for w in words)
        
        # Check 5: Does it have location/organization indicators?
        location_words = {'delhi', 'mumbai', 'india', 'bangalore', 'chennai', 'kolkata',
                         'hyderabad', 'pune', 'jaipur', 'metro', 'airport', 'station',
                         'hospital', 'school', 'court', 'police', 'government', 'ministry',
                         'isro', 'nasa', 'rbi', 'sebi'}
        has_location = any(w in location_words for w in words)
        
        # Check 6: Does it have numbers? (News often has stats)
        has_numbers = any(re.search(r'\d', w) for w in words)
        
        # SCORING: Headlines need STRONG signals
        # Proper nouns + strong action = definitely news
        # Proper nouns + location = probably news
        # Weak action alone = NOT enough
        
        score = 0
        if has_proper_nouns: score += 1
        if has_strong_action: score += 1.5  # Strong actions worth more
        if has_location: score += 1
        if has_numbers: score += 0.5
        
        # If has weak action but no strong signals, reduce score
        if has_weak_action and not has_strong_action and not has_proper_nouns:
            score -= 0.5
        
        # Need score >= 2 to be valid headline
        if score >= 2:
            return True, 1.0, None
        
        # If score is low and text is longer than typical headline, reject
        if len(words) >= 5 and score < 1.5:
            return False, 0.18, "Text lacks news structure (no recognizable names, actions, or places)"
        
        # Short text with some structure - allow through but with lower quality
        if len(words) <= 6 and score >= 1:
            return True, 0.7, None
        
        return True, 1.0, None
    
    def _check_gibberish_patterns(self, text):
        text_lower = text.lower()
        
        keyboard_patterns = ['qwerty', 'asdf', 'zxcv', 'ghjk', 'lorem ipsum']
        for pattern in keyboard_patterns:
            if pattern in text_lower:
                return False, 0.05, "Keyboard mashing or placeholder text detected"
        
        for bigram in self.gibberish_bigrams:
            if bigram in text_lower:
                return False, 0.18, "Nonsense word combination detected"
        
        words = text_lower.split()
        if len(words) >= 4:
            connectors = {'in', 'on', 'at', 'to', 'for', 'with', 'from', 'and', 'but', 'or', 'of', 'the', 'a', 'an', 'is', 'are', 'was', 'were'}
            has_connectors = any(w in connectors for w in words)
            
            strong_verbs = {'is', 'are', 'was', 'were', 'has', 'have', 'had', 'said', 'did', 'does', 'do', 'made', 'took', 'came', 'went', 'reported', 'announced', 'launches', 'connecting'}
            has_verbs = any(w in strong_verbs for w in words)
            
            proper_nouns = re.findall(self.proper_noun_pattern, text)
            
            # Only reject if NO connectors AND NO verbs AND NO proper nouns AND long
            if not has_connectors and not has_verbs and len(proper_nouns) == 0 and len(words) > 6:
                return False, 0.15, "Text appears to be random word salad"
        
        return True, 1.0, None
    
    def _calculate_quality_score(self, text, words, vectorized_features):
        valid_chars = sum(c.isalpha() or c.isdigit() or c.isspace() for c in text)
        alpha_ratio = valid_chars / len(text) if text else 0
        
        if issparse(vectorized_features):
            non_zero_features = vectorized_features.nnz
            total_features = vectorized_features.shape[1]
        else:
            non_zero_features = np.count_nonzero(vectorized_features)
            total_features = vectorized_features.shape[1]
        
        feature_density = non_zero_features / total_features if total_features > 0 else 0
        
        words_lower = set(word.lower() for word in words)
        common_found = len(words_lower.intersection(self.common_words))
        
        vowels = set('aeiou')
        words_with_vowels = sum(1 for word in words if any(c in vowels for c in word.lower()))
        vowel_ratio = words_with_vowels / len(words) if words else 0
        
        # Headline structure bonus
        headline_bonus = 0.0
        for pattern in self.headline_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                headline_bonus = 0.15
                break
        
        quality_score = min(1.0, (
            alpha_ratio * 0.20 +
            min(feature_density * 500, 1.0) * 0.20 +
            min(common_found / 1, 1.0) * 0.25 +
            min(vowel_ratio * 1.5, 1.0) * 0.20 +
            headline_bonus
        ))
        
        return quality_score