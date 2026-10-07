"use client";

import React from "react";
import { Plane, ExternalLink, Heart, Sparkles, Code2 } from "lucide-react";

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-white/10 bg-slate-950/80 backdrop-blur-xl mt-20 pt-16 pb-12">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 pb-12 border-b border-white/10">
          {/* Col 1: Brand & Bio */}
          <div className="md:col-span-5 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-sky-500 to-blue-600 flex items-center justify-center text-white shadow-[0_0_20px_rgba(56,189,248,0.3)]">
                <Plane className="w-5 h-5 -rotate-45" />
              </div>
              <span className="text-2xl font-black tracking-wider text-white">AIRLYTICS</span>
            </div>

            <p className="text-sm text-slate-400 max-w-sm leading-relaxed">
              Intelligent Airfare Price Estimation &amp; Explainable Flight Analytics. Designed for reliable price discovery and algorithmic transparency.
            </p>

            <div className="flex items-center gap-3 pt-2">
              <a
                href="https://github.com/Premanshu-Kumar/Airlytics"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 border border-white/10 hover:border-sky-400/40 text-xs font-semibold text-slate-300 hover:text-white transition-all"
              >
                <Code2 className="w-4 h-4 text-sky-400" />
                <span>GitHub Repository</span>
                <ExternalLink className="w-3 h-3 text-slate-500" />
              </a>
            </div>
          </div>

          {/* Col 2: Navigation Links */}
          <div className="md:col-span-3 space-y-3">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
              Platform Modules
            </span>
            <ul className="space-y-2 text-sm text-slate-400">
              <li>
                <a href="#predict" className="hover:text-sky-300 transition-colors">
                  Flight Price Predictor
                </a>
              </li>
              <li>
                <a href="#shap-explanation" className="hover:text-sky-300 transition-colors">
                  Why This Price? (SHAP)
                </a>
              </li>
              <li>
                <a href="#analytics" className="hover:text-sky-300 transition-colors">
                  Market Price Analytics
                </a>
              </li>
              <li>
                <a href="#routes" className="hover:text-sky-300 transition-colors">
                  Domestic Route Corridors
                </a>
              </li>
              <li>
                <a href="#model" className="hover:text-sky-300 transition-colors">
                  AI Model Benchmarks
                </a>
              </li>
            </ul>
          </div>

          {/* Col 3: Tech Stack */}
          <div className="md:col-span-4 space-y-3">
            <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
              Core Technologies
            </span>
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Next.js (React 19)
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                TypeScript
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Tailwind CSS
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Framer Motion
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Python FastAPI
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Scikit-Learn (Random Forest)
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Tree SHAP (XAI)
              </span>
              <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-white/5 text-slate-300 font-mono">
                Pytest (93 Tests)
              </span>
            </div>
          </div>
        </div>

        {/* Bottom Credits */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2026 Airlytics • Intelligent Airfare Price Estimation. Built by Premanshu Kumar.</p>
          <div className="flex items-center gap-1">
            <span>Verified 93/93 Test Suite Passed</span>
            <span className="text-emerald-400">●</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
