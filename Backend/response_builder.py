"""
Response Builder Module
Generates human-readable responses and analysis notes
"""


class ResponseBuilder:
    """Builds the final response with explanations"""
    
    @staticmethod
    def build_indeterminate_response(quality_score, validation_reason, text_length):
        """Build response for invalid/gibberish input"""
        return {
            'prediction': 'Indeterminate',
            'confidence': int(quality_score * 100),
            'confidence_percentage': int(quality_score * 100),
            'reason': f"⚠️ INPUT VALIDATION FAILED: {validation_reason}. The system cannot reliably classify this content as it does not appear to be meaningful news text.",
            'model_votes': {
                'LinearSVC': 'Unable to classify',
                'Logistic Regression': 'Unable to classify',
                'Gradient Boosting': 'Unable to classify'
            },
            'model_agreement': '0%',
            'analysis_notes': [
                f"❌ Input Quality Issue: {validation_reason}",
                f"Quality Score: {quality_score:.2f}/1.00 (threshold: 0.20)",
                "Please provide meaningful news text with proper words and grammar.",
                "The input appears to be gibberish, random characters, or severely malformed text."
            ],
            'indian_context': {
                'source_credibility': 'N/A',
                'sensationalism_score': 0,
                'has_implausible_claims': False,
                'override_applied': True
            },
            'input_validation': {
                'is_valid': False,
                'quality_score': round(quality_score, 3),
                'issue': validation_reason,
                'recommendation': 'Provide at least 3 meaningful words in proper language'
            },
            'decision_score': 0.0,
            'metadata': {
                'ensemble_used': False,
                'models_count': 0,
                'input_length': text_length,
                'dataset': 'IFND (Indian Fake News Dataset)',
                'validation_failed': True
            }
        }
    
    @staticmethod
    def build_normal_response(prediction, confidence, model_votes, agreement, 
                            credibility, sensationalism, implausible, override,
                            quality_score, web, category, text_length, decision_score):
        """Build normal response for valid input"""
        result = 'Fake' if prediction == 1 else 'Real'
        credibility_text = "TRUSTED" if credibility > 0 else ("SUSPICIOUS" if credibility < 0 else "UNKNOWN")
        
        reason = ResponseBuilder._generate_reason(
            prediction, confidence, credibility, sensationalism, 
            implausible, quality_score
        )
        
        analysis_notes = ResponseBuilder._generate_analysis_notes(
            web, category, sensationalism, implausible, model_votes,
            override, credibility_text, quality_score
        )
        
        return {
            'prediction': result,
            'confidence': confidence,
            'confidence_percentage': confidence,
            'reason': reason,
            'model_votes': model_votes,
            'model_agreement': agreement,
            'analysis_notes': analysis_notes,
            'indian_context': {
                'source_credibility': credibility_text,
                'sensationalism_score': round(sensationalism, 1),
                'has_implausible_claims': implausible,
                'override_applied': override['applied']
            },
            'input_validation': {
                'is_valid': True,
                'quality_score': round(quality_score, 3),
                'issue': None
            },
            'decision_score': decision_score,
            'metadata': {
                'ensemble_used': True,
                'models_count': 3,
                'input_length': text_length,
                'dataset': 'IFND (Indian Fake News Dataset)'
            }
        }
    
    @staticmethod
    def _generate_reason(prediction, confidence, credibility, sensationalism, 
                        implausible, quality_score):
        """Generate explanation text"""
        credibility_text = "TRUSTED" if credibility > 0 else ("SUSPICIOUS" if credibility < 0 else "UNKNOWN")
        
        if prediction == 1:  # FAKE
            if confidence >= 85:
                reason = "🚨 HIGH CONFIDENCE FAKE NEWS. All or most models agree this is misinformation. "
            elif confidence >= 70:
                reason = "⚠️ LIKELY FAKE NEWS. Multiple models indicate this may be false. "
            else:
                reason = "⚡ POSSIBLY FAKE NEWS. Models show mixed signals. "
            
            if credibility < 0:
                reason += "The source is flagged as SUSPICIOUS. "
            elif credibility == 0:
                reason += "The source is UNKNOWN or UNVERIFIED. "
            
            if sensationalism > 5:
                reason += f"High sensationalism detected (score: {sensationalism:.1f}/10). "
            
            if implausible:
                reason += "Contains IMPLAUSIBLE CLAIMS that are commonly found in fake news. "
            
            reason += "Please verify with trusted Indian news sources before sharing."
        
        else:  # REAL
            if confidence >= 85:
                reason = "✅ HIGH CONFIDENCE REAL NEWS. All or most models agree this appears credible. "
            elif confidence >= 70:
                reason = "✓ LIKELY REAL NEWS. Multiple indicators suggest this is legitimate. "
            else:
                reason = "🤔 POSSIBLY REAL NEWS. Models show mixed signals. "
            
            if credibility > 0:
                reason += "Source is a TRUSTED Indian news outlet. "
            
            if sensationalism < 3:
                reason += f"Low sensationalism (score: {sensationalism:.1f}/10). "
            
            reason += "However, always cross-verify important news with multiple sources."
        
        if quality_score < 0.6:
            reason += f" Note: Input quality score is moderate ({quality_score:.2f}/1.00)."
        
        return reason
    
    @staticmethod
    def _generate_analysis_notes(web, category, sensationalism, implausible, 
                                model_votes, override, credibility_text, quality_score):
        """Generate bullet point analysis"""
        notes = []
        
        notes.append(f"✓ Input Quality Score: {quality_score:.2f}/1.00")
        
        if web:
            notes.append(f"Source: {web} (Credibility: {credibility_text})")
        
        if category:
            notes.append(f"Category: {category}")
        
        notes.append(f"Sensationalism Score: {sensationalism:.1f}/10")
        
        if implausible:
            notes.append("⚠️ Contains implausible claims")
        
        # Count votes
        fake_votes = sum(1 for v in model_votes.values() if v == 'Fake')
        real_votes = 3 - fake_votes
        
        if fake_votes == 3:
            notes.append("Unanimous: All 3 models say FAKE")
        elif real_votes == 3:
            notes.append("Unanimous: All 3 models say REAL")
        else:
            notes.append(f"Split: {fake_votes} FAKE, {real_votes} REAL")
        
        if override['applied']:
            notes.append(f"🛡️ Override applied: {override['reason']}")
        
        return notes