import { useState } from 'react';
import { motion } from 'motion/react';
import { Scale, Sparkles, Shield, ChevronDown, Loader2 } from 'lucide-react';
import { Scene3D } from './components/Scene3D';
import { RiskOutputCard } from './components/RiskOutput';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000';

function App() {
  const [clauseText, setClauseText] = useState('');
  const [result, setResult] = useState<{ risk: 'Low' | 'Medium' | 'High'; explanation: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSimplify = async () => {
    if (!clauseText.trim()) return;
    
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/simplify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clause: clauseText }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail ?? 'Failed to simplify clause');
      }

      const data = await response.json();
      setResult({
        risk: data.risk as 'Low' | 'Medium' | 'High',
        explanation: data.explanation as string,
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Something went wrong');
    } finally {
      setIsLoading(false);
    }
  };

  const scrollToApp = () => {
    const appSection = document.getElementById('app-section');
    appSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-x-hidden">
      <style>{`
        @keyframes pulse-glow {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.8; }
        }
        .animate-pulse-glow {
          animation: pulse-glow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        .glass-card {
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 24px;
          box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        .glass-input {
          background: rgba(255, 255, 255, 0.03);
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 16px;
          transition: all 0.3s ease;
        }
        .glass-input:focus {
          background: rgba(255, 255, 255, 0.08);
          border-color: rgba(99, 102, 241, 0.5);
          box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
          outline: none;
        }
        .glass-button {
          background: linear-gradient(135deg, rgba(99, 102, 241, 0.8) 0%, rgba(139, 92, 246, 0.8) 100%);
          backdrop-filter: blur(16px);
          -webkit-backdrop-filter: blur(16px);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 16px;
          box-shadow: 0 8px 32px 0 rgba(99, 102, 241, 0.4);
          transition: all 0.3s ease;
        }
        .glass-button:hover:not(:disabled) {
          transform: translateY(-2px) scale(1.02);
          box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.6);
          background: linear-gradient(135deg, rgba(99, 102, 241, 1) 0%, rgba(139, 92, 246, 1) 100%);
        }
        .glass-button:active:not(:disabled) {
          transform: translateY(0) scale(0.98);
        }
        .mesh-gradient-bg {
          background: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.3) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.3) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.3) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(99, 102, 241, 0.3) 0px, transparent 50%);
        }
      `}</style>

      {/* Hero Section */}
      <div className="relative min-h-screen flex items-center justify-center px-6 mesh-gradient-bg">
        {/* 3D Background */}
        <div className="absolute inset-0 opacity-40">
          <Scene3D />
        </div>

        {/* Hero Content */}
        <div className="relative z-10 max-w-6xl mx-auto text-center space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card"
          >
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="text-sm text-indigo-300 font-medium">AI-Powered Legal Analysis</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl md:text-7xl lg:text-8xl font-bold leading-tight"
          >
            <span className="bg-gradient-to-br from-white via-white/90 to-white/70 bg-clip-text text-transparent">
              Legal Clause
            </span>
            <br />
            <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-blue-400 bg-clip-text text-transparent">
              Simplifier
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-lg md:text-xl text-white/60 max-w-3xl mx-auto"
          >
            Transform complex rental agreement clauses into plain English
            with AI-powered risk assessment—completely local and private.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="flex items-center justify-center gap-6 pt-8"
          >
            <button
              onClick={scrollToApp}
              className="glass-button px-8 py-4 text-white font-semibold text-lg flex items-center gap-3"
            >
              <Scale className="w-5 h-5" />
              Try It Now
            </button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1, delay: 1 }}
            className="absolute bottom-12 left-1/2 -translate-x-1/2"
          >
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="cursor-pointer"
              onClick={scrollToApp}
            >
              <ChevronDown className="w-8 h-8 text-white/40" />
            </motion.div>
          </motion.div>
        </div>

        {/* Floating Elements */}
        <motion.div
          animate={{
            y: [0, -20, 0],
            rotate: [0, 5, 0],
          }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-1/4 left-[10%] glass-card p-6 hidden lg:block"
        >
          <Shield className="w-12 h-12 text-indigo-400" />
        </motion.div>

        <motion.div
          animate={{
            y: [0, 20, 0],
            rotate: [0, -5, 0],
          }}
          transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
          className="absolute bottom-1/4 right-[10%] glass-card p-6 hidden lg:block"
        >
          <Scale className="w-12 h-12 text-purple-400" />
        </motion.div>
      </div>

      {/* Main App Section */}
      <div id="app-section" className="min-h-screen py-20 px-6 bg-slate-900">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
            {/* Left Column - 3D Element */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="relative h-[600px] glass-card overflow-hidden"
            >
              <Scene3D />
              <div className="absolute bottom-8 left-8 right-8 glass-card p-6">
                <h3 className="text-xl font-semibold text-white mb-2">Local AI Model</h3>
                <p className="text-white/60 text-sm">
                  Powered by Gemma 3 270M running locally on your machine.
                  No data leaves your device. Complete privacy guaranteed.
                </p>
              </div>
            </motion.div>

            {/* Right Column - Input & Output */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <div className="glass-card p-8 space-y-6">
                <div>
                  <label className="block text-white/90 font-semibold mb-3 text-lg">
                    Paste Your Rental Clause
                  </label>
                  <textarea
                    value={clauseText}
                    onChange={(e) => setClauseText(e.target.value)}
                    placeholder="Example: The tenant must provide written notice of at least 30 days prior to vacating the premises..."
                    className="glass-input w-full h-48 px-6 py-4 text-white placeholder-white/30 resize-none"
                  />
                </div>

                <button
                  onClick={handleSimplify}
                  disabled={!clauseText.trim() || isLoading}
                  className="glass-button w-full py-4 text-white font-semibold text-lg flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      Analyzing Clause...
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-5 h-5" />
                      Simplify Clause
                    </>
                  )}
                </button>
              </div>

              {error && (
                <div className="glass-card p-6 border border-red-500/40">
                  <p className="text-red-300 text-sm">{error}</p>
                </div>
              )}

              {/* Output Area */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="glass-card p-8 flex items-center justify-center"
                >
                  <div className="text-center space-y-4">
                    <Loader2 className="w-12 h-12 text-indigo-400 animate-spin mx-auto" />
                    <p className="text-white/60">Processing your clause with local AI...</p>
                  </div>
                </motion.div>
              )}

              {result && !isLoading && (
                <RiskOutputCard risk={result.risk} explanation={result.explanation} />
              )}

              {!result && !isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="glass-card p-8 text-center"
                >
                  <Scale className="w-16 h-16 text-white/20 mx-auto mb-4" />
                  <p className="text-white/40">
                    Enter a rental clause above to get started
                  </p>
                </motion.div>
              )}
            </motion.div>
          </div>

          {/* Features Section */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20"
          >
            {[
              {
                icon: Shield,
                title: '100% Private',
                description: 'All processing happens locally. Your clauses never leave your device.',
              },
              {
                icon: Sparkles,
                title: 'AI-Powered',
                description: 'Fine-tuned Gemma 3 model specifically trained on legal documents.',
              },
              {
                icon: Scale,
                title: 'Risk Assessment',
                description: 'Automatic risk level detection: Low, Medium, or High.',
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass-card p-8 text-center space-y-4 hover:scale-105 transition-transform"
              >
                <feature.icon className="w-12 h-12 text-indigo-400 mx-auto" />
                <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Footer */}
      <div className="py-12 px-6 border-t border-white/10 bg-slate-950">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-white/40 text-sm">
            Legal Clause Simplifier • Powered by Gemma 3 270M • 100% Local & Private
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
