import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';

const FakeNewsDetector = () => {
  const [text, setText] = useState('');
  const [web, setWeb] = useState('');
  const [category, setCategory] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const categories = ['COVID-19', 'ELECTION', 'POLITICS', 'TERROR', 'VIOLENCE', 'SPORTS', 'ENTERTAINMENT', 'HEALTH', 'RELIGION', 'GOVERNMENT'];

  const checkNews = async () => {
    setResult(null);
    setError('');

    if (!text.trim()) {
      setError('Please enter some news text');
      return;
    }

    setLoading(true);

    try {
      const API_BASE = 'http://127.0.0.1:5000';

      const response = await fetch(`${API_BASE}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text.trim(),
          web: web.trim() || undefined,
          category: category || undefined
        })
      });

      const data = await response.json();

      if (response.ok) {
        let confidenceValue = 0;
        
        if (typeof data.confidence === 'number') {
          confidenceValue = data.confidence;
        } else if (typeof data.confidence === 'string') {
          confidenceValue = parseInt(data.confidence.split('/')[0]) || 0;
        } else if (data.confidence_percentage) {
          confidenceValue = data.confidence_percentage;
        }

        const isFake = data.prediction === 'Fake' || data.prediction === 'fake';
        const isIndeterminate = data.prediction === 'Indeterminate';
        
        setResult({
          verdict: isIndeterminate ? 'Indeterminate' : (isFake ? 'Fake News' : 'Real News'),
          isFake: isFake,
          isIndeterminate: isIndeterminate,
          reason: data.reason,
          confidence: confidenceValue,
          analysis_notes: data.analysis_notes || [],
          indian_context: data.indian_context || {},
          input_validation: data.input_validation || null
        });
      } else {
        setError(data.error || 'Something went wrong.');
      }
    } catch (err) {
      setError('⚠️ Could not connect to the server. Please ensure the backend is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setText('');
    setWeb('');
    setCategory('');
    setResult(null);
    setError('');
  };

  const ConfidenceWaterTank = ({ confidence, isFake, isIndeterminate }) => {
    const [currentFill, setCurrentFill] = useState(0);
    const [waveOffset, setWaveOffset] = useState(0);
    const [showPercentage, setShowPercentage] = useState(false);

    // Animate water filling progressively from 0 to target percentage
    useEffect(() => {
      setCurrentFill(0);
      setShowPercentage(false);
      
      const fillDuration = 2000; // 2 seconds to fill
      const startTime = Date.now();
      
      const animateFill = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / fillDuration, 1);
        
        // Ease-out function for smooth deceleration
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        setCurrentFill(easeProgress * confidence);
        
        if (progress < 1) {
          requestAnimationFrame(animateFill);
        } else {
          // Show percentage after fill completes
          setTimeout(() => setShowPercentage(true), 300);
        }
      };
      
      requestAnimationFrame(animateFill);
    }, [confidence]);

    useEffect(() => {
      let frame = 0;
      const animate = () => {
        frame += 0.05;
        setWaveOffset(Math.sin(frame) * 3);
        requestAnimationFrame(animate);
      };
      const id = requestAnimationFrame(animate);
      return () => cancelAnimationFrame(id);
    }, []);

    let gradientColors = 'from-emerald-400 to-emerald-600';
    let glowColor = 'rgba(16, 185, 129, 0.4)';
    
    if (isIndeterminate) {
      gradientColors = 'from-yellow-400 to-amber-500';
      glowColor = 'rgba(251, 191, 36, 0.4)';
    } else if (isFake) {
      gradientColors = 'from-rose-400 to-rose-600';
      glowColor = 'rgba(244, 63, 94, 0.4)';
    }

    return (
      <div className="flex flex-col items-center gap-4 mb-6">
        <div className="relative w-28 h-48 rounded-3xl border-2 border-neutral-700 bg-neutral-950 overflow-hidden shadow-2xl">
          
          {/* Water fills from bottom to top, showing the rising level */}
          <div
            className={`absolute left-0 w-full bg-gradient-to-b ${gradientColors}`}
            style={{
              bottom: 0,
              height: `${currentFill}%`,
              opacity: 0.85,
              transition: 'none', // Remove CSS transition, using JS animation instead
            }}
          >
            {/* Ripple effect at water surface */}
            {currentFill > 0 && currentFill < confidence && (
              <div className="absolute inset-x-0 top-0 h-8 bg-gradient-to-b from-white/30 to-transparent animate-pulse" />
            )}
            
            {/* Bubbles effect */}
            <div className="absolute inset-0 opacity-20">
              <div className="absolute w-2 h-2 bg-white rounded-full animate-bubble-1" style={{ left: '20%', bottom: '10%' }} />
              <div className="absolute w-1.5 h-1.5 bg-white rounded-full animate-bubble-2" style={{ left: '60%', bottom: '5%' }} />
              <div className="absolute w-1 h-1 bg-white rounded-full animate-bubble-3" style={{ left: '80%', bottom: '15%' }} />
            </div>
          </div>

          {/* Wave effect at the top surface of water */}
          <div
            className="absolute left-0 w-full h-4 opacity-70 pointer-events-none"
            style={{
              bottom: `calc(${currentFill}% - 8px)`,
              transform: `translateY(${waveOffset}px)`,
            }}
          >
            <svg viewBox="0 0 1200 120" preserveAspectRatio="none" className="w-full h-full">
              <path
                d="M0,60 Q150,40 300,60 T600,60 T900,60 T1200,60 L1200,120 L0,120 Z"
                fill="currentColor"
                className="text-white/30"
              />
            </svg>
          </div>

          {/* Glass shine */}
          <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-transparent pointer-events-none rounded-3xl" />
          
          {/* Light reflection */}
          <div className="absolute top-4 left-4 w-8 h-12 bg-white/10 rounded-full blur-md" />

          {/* Glow when filled */}
          {currentFill > 20 && (
            <div 
              className="absolute inset-0 pointer-events-none rounded-3xl"
              style={{
                boxShadow: `inset 0 0 30px ${glowColor}, 0 0 20px ${glowColor}`
              }}
            />
          )}

          {/* Percentage - appears after fill animation completes */}
          <div className={`absolute inset-0 flex items-center justify-center z-10 transition-opacity duration-500 ${showPercentage ? 'opacity-100' : 'opacity-0'}`}>
            <span className="text-2xl font-bold text-white drop-shadow-lg">
              {Math.round(confidence)}%
            </span>
          </div>
        </div>

        <p className="text-xs tracking-widest text-neutral-400 font-semibold">
          CONFIDENCE LEVEL
        </p>
      </div>
    );
  };

  return (
    <div className="min-h-screen w-full bg-neutral-950 text-neutral-100">
      
      <div className="fixed inset-0 pointer-events-none opacity-[0.03]">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.1)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.1)_1px,transparent_1px)] bg-[size:64px_64px] animate-grid" />
      </div>

      <div className="max-w-7xl mx-auto px-6 py-16 grid grid-cols-1 lg:grid-cols-2 gap-16 relative">

        <div className="flex flex-col justify-center space-y-6">
          <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-400/20 text-indigo-300 text-sm w-fit">
            <Shield className="w-4 h-4" />
            AI Credibility System
          </div>

          <h1 className="text-5xl font-semibold leading-tight">
            Detect fake news
            <br />
            <span className="text-neutral-400">before it misleads</span>
          </h1>

          <p className="text-neutral-400 max-w-lg leading-relaxed">
            Analyze news content using ensemble ML models, source credibility scoring,
            and Indian context awareness — designed for informed decision-making.
          </p>

          <div className="flex gap-6 pt-4 text-sm text-neutral-500">
            <span>✔ 3 ML Models</span>
            <span>✔ Source-aware</span>
            <span>✔ Explainable</span>
          </div>
        </div>

        <div className="bg-neutral-900/60 backdrop-blur-xl rounded-3xl border border-neutral-800 p-8 space-y-6 shadow-2xl">
          
          <div className="space-y-1">
            <h2 className="text-xl font-semibold">Analyze content</h2>
            <p className="text-sm text-neutral-400">Paste news text to verify</p>
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={6}
            className="w-full rounded-2xl px-5 py-4 bg-neutral-950/70 border border-neutral-700/50 placeholder-neutral-500 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/30 resize-none transition-all"
            placeholder="Paste headline or article text here..."
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <input
    value={web}
    onChange={(e) => setWeb(e.target.value)}
    className="rounded-xl px-4 py-3 bg-neutral-950/70 border border-neutral-700/50 focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/30 transition-all"
    placeholder="Source"
  />

  <select
    value={category}
    onChange={(e) => setCategory(e.target.value)}
    className="rounded-xl px-4 py-3 bg-neutral-950/70 border border-neutral-700/50 cursor-pointer focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/30 transition-all"
  >
    <option value="">Category</option>
    {categories.map(cat => (
      <option key={cat} value={cat}>{cat}</option>
    ))}
  </select>
</div>


          {error && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3 text-red-300 text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              onClick={checkNews}
              disabled={loading || !text.trim()}
              className="flex-1 py-4 rounded-2xl font-semibold text-neutral-900 bg-gradient-to-r from-indigo-400 to-amber-400 hover:from-indigo-300 hover:to-amber-300 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3 shadow-lg hover:shadow-xl"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-neutral-700 border-t-neutral-900 rounded-full animate-spin" />
                  Analyzing…
                </>
              ) : (
                <>Run Analysis</>
              )}
            </button>
            
            {result && (
              <button
                onClick={resetAnalysis}
                className="px-6 py-4 rounded-2xl font-semibold text-neutral-300 bg-neutral-800 hover:bg-neutral-700 transition-all flex items-center justify-center gap-2 shadow-lg hover:shadow-xl"
              >
                New Analysis
              </button>
            )}
          </div>
        </div>
      </div>

      {result && (
        <div className="max-w-5xl mx-auto px-6 pb-16">
          <div className="bg-neutral-900/70 border border-neutral-800 rounded-3xl p-8 shadow-2xl animate-slideIn">
            
            <div className="flex flex-col items-center text-center mb-6">
              <ConfidenceWaterTank
                confidence={result.confidence}
                isFake={result.isFake}
                isIndeterminate={result.isIndeterminate}
              />

              <div className="flex items-center gap-3 mb-2">
                {result.isIndeterminate ? (
                  <AlertTriangle className="w-8 h-8 text-yellow-400" />
                ) : result.isFake ? (
                  <AlertTriangle className="w-8 h-8 text-rose-400" />
                ) : (
                  <CheckCircle className="w-8 h-8 text-emerald-400" />
                )}
                
                <h3 className={`text-3xl font-semibold ${
                  result.isIndeterminate ? 'text-yellow-400' : 
                  result.isFake ? 'text-rose-400' : 'text-emerald-400'
                }`}>
                  {result.verdict}
                </h3>
              </div>

              <p className="text-sm text-neutral-400 mb-4">
                {result.isIndeterminate ? 'Input quality issue detected' : 'AI-powered assessment'}
              </p>
            </div>

            <div className="bg-neutral-950/50 rounded-2xl p-6 mb-6">
              <p className="text-neutral-200 leading-relaxed text-sm">
                {result.reason}
              </p>
            </div>

            {result.analysis_notes && result.analysis_notes.length > 0 && (
              <div className="bg-neutral-950/50 rounded-2xl border border-neutral-800/50 p-6 space-y-3">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-1 h-5 bg-gradient-to-b from-indigo-400 to-amber-400 rounded-full" />
                  <h4 className="text-sm font-semibold text-neutral-300 tracking-wide">ANALYSIS INSIGHTS</h4>
                </div>
                
                <div className="space-y-2.5">
                  {result.analysis_notes.map((note, idx) => (
                    <div key={idx} className="flex items-start gap-3 text-sm text-neutral-300 bg-neutral-900/40 rounded-xl px-4 py-3 border border-neutral-800/30">
                      <span className="text-indigo-400 mt-0.5 font-bold">→</span>
                      <span className="leading-relaxed">{note}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <style>{`
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-slideIn {
          animation: slideIn 1.8s ease-out;
        }

        @keyframes grid {
          0% { transform: translateY(0); }
          100% { transform: translateY(64px); }
        }

        .animate-grid {
          animation: grid 20s linear infinite;
        }

        @keyframes bubble-1 {
          0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
          50% { transform: translateY(-80px) scale(1.2); opacity: 0; }
        }

        @keyframes bubble-2 {
          0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
          50% { transform: translateY(-60px) scale(1.1); opacity: 0; }
        }

        @keyframes bubble-3 {
          0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
          50% { transform: translateY(-100px) scale(1.3); opacity: 0; }
        }

        .animate-bubble-1 {
          animation: bubble-1 3s ease-in-out infinite;
        }

        .animate-bubble-2 {
          animation: bubble-2 4s ease-in-out infinite 0.5s;
        }

        .animate-bubble-3 {
          animation: bubble-3 3.5s ease-in-out infinite 1s;
        }
      `}</style>
    </div>
  );
};

export default FakeNewsDetector;