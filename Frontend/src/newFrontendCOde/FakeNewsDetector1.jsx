import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle, 
  Sparkles, 
  Globe, 
  Search,
  FileText,
  TrendingUp,
  MapPin,
  Loader2
} from 'lucide-react';
import ConfidenceGauge from './ConfidenceGauge';
import AnalysisCard from './AnalysisCard';
import CategoryBadge from './CategoryBadge';

const FakeNewsDetector1 = () => {
  const [text, setText] = useState('');
  const [web, setWeb] = useState('');
  const [category, setCategory] = useState('');
  const [result, setResult] = useState(null); // <-- removed TypeScript annotation
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const categories = [ 'ELECTION', 'POLITICS', 'TERROR', 'VIOLENCE', 'SPORTS', 'ENTERTAINMENT', 'HEALTH', 'RELIGION','GOVERNMENT'];

  const checkNews = async () => {
    setResult(null);
    setError('');

    if (!text.trim()) {
      setError('Please enter some news text to analyze');
      return;
    }

    setLoading(true);

    // Simulating API call
    setTimeout(() => {
      const isFake = Math.random() > 0.5;
      setResult({
        verdict: isFake ? 'Likely Fake' : 'Likely Authentic',
        isFake: isFake,
        reason: isFake 
          ? 'This content exhibits multiple characteristics commonly associated with misinformation, including sensationalized language, unverifiable claims, and inconsistencies with established facts from credible sources.'
          : 'This content demonstrates hallmarks of authentic journalism: verified sources, consistent factual claims, balanced reporting, and alignment with reports from established news outlets.',
        confidence: Math.floor(Math.random() * 25) + 75,
        analysis_notes: isFake ? [
          'No verification from official sources or agencies',
          'Excessive use of emotional and sensational language',
          'Missing specific details, timestamps, or attributions',
          'Source has limited credibility history'
        ] : [
          'Cross-verified with multiple credible sources',
          'Facts align with official records and reports',
          'Proper journalistic attribution and citations',
          'No signs of manipulation or misleading context'
        ],
        indian_context: {
          source_credibility: isFake ? 'UNVERIFIED' : 'VERIFIED',
          regional_relevance: 'High'
        }
      });
      setLoading(false);
    }, 2000);
  };

  const getCredibilityStyles = (credibility) => { // removed type annotation
    if (credibility === 'VERIFIED') return 'bg-success/10 text-success border-success/20';
    if (credibility === 'UNVERIFIED') return 'bg-destructive/10 text-destructive border-destructive/20';
    return 'bg-warning/10 text-warning border-warning/20';
  };

  return (
  <div className="min-h-screen bg-slate-50">
    {/* Subtle Grid Background */}
    <div className="fixed inset-0 bg-[linear-gradient(to_right,#e5e7eb_1px,transparent_1px),linear-gradient(to_bottom,#e5e7eb_1px,transparent_1px)] bg-[size:32px_32px] opacity-40 pointer-events-none" />

    <div className="relative container max-w-6xl mx-auto px-4 py-10">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="mb-12 grid grid-cols-1 md:grid-cols-12 gap-6 items-center"
      >
        <div className="md:col-span-8">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 tracking-tight">
            Fake News Detector
          </h1>
          <p className="mt-3 text-lg text-slate-600 max-w-xl">
            Verify news content using AI-driven linguistic and contextual analysis
          </p>
        </div>

        <div className="md:col-span-4 flex md:justify-end">
          <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-5 py-3 shadow-sm">
            <Shield className="w-6 h-6 text-indigo-600" />
            <span className="text-sm font-semibold text-slate-700">
              Trusted AI Analysis
            </span>
          </div>
        </div>
      </motion.div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Input Panel */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 shadow-sm p-6"
        >
          <div className="space-y-6">
            {/* News Input */}
            <div>
              <label className="text-sm font-semibold text-slate-800 flex items-center gap-2 mb-2">
                <FileText className="w-4 h-4 text-indigo-500" />
                News Content
              </label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={5}
                placeholder="Paste the headline or full article text here…"
                className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition resize-none"
              />
            </div>

            {/* Meta Inputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="text-sm font-semibold text-slate-800 mb-2 flex items-center gap-2">
                  <Globe className="w-4 h-4 text-slate-500" />
                  Source
                </label>
                <input
                  value={web}
                  onChange={(e) => setWeb(e.target.value)}
                  placeholder="e.g. Reuters, NDTV"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition"
                />
              </div>

              <div>
                <label className="text-sm font-semibold text-slate-800 mb-2 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-slate-500" />
                  Category
                </label>
                <div className="flex flex-wrap gap-2">
                  {categories.slice(0, 5).map((cat) => (
                    <CategoryBadge
                      key={cat}
                      category={cat}
                      selected={category === cat}
                      onClick={() =>
                        setCategory(category === cat ? '' : cat)
                      }
                    />
                  ))}
                </div>
              </div>
            </div>

            {/* Action */}
            <button
              onClick={checkNews}
              disabled={loading || !text.trim()}
              className="w-full h-12 rounded-xl bg-indigo-600 text-white font-semibold
              hover:bg-indigo-700 transition
              disabled:opacity-50 disabled:cursor-not-allowed
              flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing…
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Analyze News
                </>
              )}
            </button>
          </div>

          {/* Error */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4"
              >
                <div className="flex gap-3 items-center">
                  <AlertTriangle className="w-5 h-5 text-red-500" />
                  <p className="text-sm font-medium text-red-700">
                    {error}
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        {/* Results Panel */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 shadow-sm p-6"
            >
              <div className="space-y-6">
                {/* Verdict */}
                <div className="text-center">
                  <ConfidenceGauge
                    confidence={result.confidence}
                    isFake={result.isFake}
                  />

                  <div className="mt-5">
                    {result.isFake ? (
                      <span className="inline-flex items-center gap-2 rounded-full bg-red-100 text-red-700 px-4 py-2 font-semibold">
                        <AlertTriangle className="w-5 h-5" />
                        {result.verdict}
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-2 rounded-full bg-emerald-100 text-emerald-700 px-4 py-2 font-semibold">
                        <CheckCircle className="w-5 h-5" />
                        {result.verdict}
                      </span>
                    )}
                  </div>
                </div>

                {/* Details */}
                <AnalysisCard title="Analysis Summary" icon={Sparkles}>
                  <p className="text-sm text-slate-700 leading-relaxed">
                    {result.reason}
                  </p>
                </AnalysisCard>

                {result.analysis_notes.length > 0 && (
                  <AnalysisCard title="Key Indicators" icon={FileText}>
                    <ul className="space-y-2">
                      {result.analysis_notes.map((note, idx) => (
                        <li
                          key={idx}
                          className="flex gap-3 text-sm text-slate-700"
                        >
                          <span
                            className={`mt-1.5 w-2 h-2 rounded-full ${
                              result.isFake
                                ? 'bg-red-400'
                                : 'bg-emerald-400'
                            }`}
                          />
                          {note}
                        </li>
                      ))}
                    </ul>
                  </AnalysisCard>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <p className="mt-10 text-center text-sm text-slate-500">
        AI-powered analysis • IFND dataset • NLP-based verification
      </p>
    </div>
  </div>
);

};

export default FakeNewsDetector1;
