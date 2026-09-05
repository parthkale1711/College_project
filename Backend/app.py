"""
Flask API Application
Main entry point with all API routes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

from config import model_loader
from features_refactored import FeatureProcessor, PredictionEngine

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

# Load models
model_loader.load_models()
models = model_loader.get_models()

feature_processor = FeatureProcessor(
    trusted_sources=models['trusted_sources'],
    suspicious_sources=models['suspicious_sources'],
    sensational_keywords=models['sensational_keywords']
)

prediction_engine = PredictionEngine(models, feature_processor)

# ==================== API ROUTES ====================

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        text = data.get('text', '').strip()
        web = data.get('web', '').strip()
        category = data.get('category', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"\n{'='*60}")
        print(f"NEW PREDICTION REQUEST")
        print(f"Text: {text[:60]}...")
        print(f"Web: {web}, Category: {category}")
        print(f"{'='*60}")
        
        response = prediction_engine.predict(text, web, category)
        
        print(f"FINAL RESULT: {response.get('prediction', 'N/A')} "
              f"(Confidence: {response.get('confidence', 'N/A')}%)")
        print(f"{'='*60}\n")
        
        return jsonify(response)
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"ERROR: {error_trace}")
        return jsonify({
            'error': 'An error occurred during prediction',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'models_loaded': True,
        'version': '3.2-fixed',
        'dataset': 'IFND'
    })

@app.route('/sources', methods=['GET'])
def get_sources():
    return jsonify({
        'trusted_sources': models['trusted_sources'][:20],
        'suspicious_indicators': models['suspicious_sources'],
        'total_trusted': len(models['trusted_sources']),
        'note': 'Based on IFND dataset and Indian media landscape'
    })

@app.route('/models-info', methods=['GET'])
def models_info():
    return jsonify({
        'models': ['LinearSVC', 'Logistic Regression', 'Gradient Boosting'],
        'ensemble_method': 'Majority Voting with Conservative Override',
        'vectorizer': 'TF-IDF (ngrams 1-3, 12k features)',
        'dataset': 'IFND (Indian Fake News Dataset)',
        'fixes': [
            'Text cleaning preserves numbers and punctuation',
            'Emergency news whitelisted from implausible detection',
            'Sensationalism score reduced for factual reporting',
            'Overrides now require very low confidence (<45%)',
            'Feature string repeats statement 3x for text weight'
        ]
    })

@app.route('/test-examples', methods=['GET'])
def test_examples():
    return jsonify({
        'examples': [
            {
                'text': '16, Mumbai power outage: Fire reported in hospital',
                'web': 'DNAINDIA',
                'category': 'VIOLENCE',
                'expected': 'Real'
            },
            {
                'text': 'WHO praises India\'s Aarogya Setu app, says it helped in identifying COVID-19 clusters',
                'web': 'DNAINDIA',
                'category': 'COVID-19',
                'expected': 'Real'
            },
            {
                'text': 'Scientists confirm aliens landed in New York City',
                'web': 'Unknown',
                'category': 'SCIENCE',
                'expected': 'Fake'
            },
            {
                'text': 'WhatsApp forward claims drinking cow urine cures coronavirus',
                'web': 'WhatsApp',
                'category': 'COVID-19',
                'expected': 'Fake'
            },
            {
                'text': 'Prime Minister announces new economic reforms',
                'web': 'Times of India',
                'category': 'POLITICS',
                'expected': 'Real'
            },
            {
                'text': 'Breaking: 5G towers spreading COVID-19, government confirms',
                'web': 'ViralNews',
                'category': 'COVID-19',
                'expected': 'Fake'
            }
        ]
    })

@app.route('/debug-predict', methods=['POST'])
def debug_predict():
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.json
        text = data.get('text', '').strip()
        web = data.get('web', '').strip()
        category = data.get('category', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Manual feature extraction for debugging
        credibility = feature_processor.get_source_credibility(web)
        sensationalism = feature_processor.extract_sensationalism_score(text)
        implausible = feature_processor.check_implausible_claims(text)
        cleaned = feature_processor.clean_text(text)
        features = feature_processor.create_enhanced_features(text, web, category)
        
        # Get raw model predictions
        vectorized = models['vectorizer'].transform([features])
        svc_pred = models['svc'].predict(vectorized)[0]
        lr_pred = models['lr'].predict(vectorized)[0]
        gb_pred = models['gb'].predict(vectorized)[0]
        
        # Get full prediction
        response = prediction_engine.predict(text, web, category)
        
        return jsonify({
            'input': {'text': text, 'web': web, 'category': category},
            'cleaned_text': cleaned,
            'feature_string_preview': features[:150],
            'extracted_features': {
                'credibility': credibility,
                'sensationalism': sensationalism,
                'implausible': implausible
            },
            'raw_predictions': {
                'LinearSVC': 'Fake' if svc_pred == 1 else 'Real',
                'LogisticRegression': 'Fake' if lr_pred == 1 else 'Real',
                'GradientBoosting': 'Fake' if gb_pred == 1 else 'Real'
            },
            'final_result': response
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Indian Fake News Detection API - FIXED v3.2',
        'version': '3.2',
        'dataset': 'IFND',
        'endpoints': {
            'POST /predict': 'Predict if news is fake or real',
            'POST /debug-predict': 'DEBUG: See full prediction breakdown',
            'GET /health': 'Health check',
            'GET /models-info': 'Model information',
            'GET /test-examples': 'Test examples including Mumbai fire case'
        }
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print(" INDIAN FAKE NEWS DETECTION API - v3.2 FIXED")
    print(" Dataset: IFND (2013-2021)")
    print(" Key Fix: Text cleaning preserves structure, emergency news whitelisted")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)