"use client";

import React from "react";
import { motion } from "framer-motion";
import { Plane, Compass, Sparkles, TrendingUp, ShieldCheck } from "lucide-react";

export const HeroSection: React.FC = () => {
  return (
    <section className="relative min-h-[90vh] flex flex-col items-center justify-center pt-24 pb-16 px-4 overflow-hidden">
      {/* Background radial gradient glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-sky-500/10 blur-[130px] rounded-full pointer-events-none -z-10" />
      <div className="absolute top-1/3 left-1/4 w-[350px] h-[250px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none -z-10" />

      {/* Hero Badge */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full border border-sky-400/30 bg-sky-500/10 text-sky-300 text-xs sm:text-sm font-medium tracking-wide mb-8 shadow-[0_0_15px_rgba(56,189,248,0.15)]"
      >
        <Sparkles className="w-4 h-4 text-sky-400 animate-pulse" />
        <span>Explainable Machine Learning • Random Forest Ensemble</span>
        <span className="hidden sm:inline-block w-1.5 h-1.5 rounded-full bg-sky-400/60" />
        <span className="hidden sm:inline text-sky-200/80">R² 0.9019</span>
      </motion.div>

      {/* Main Headline */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
        className="text-center max-w-4xl mx-auto"
      >
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-slate-100 uppercase leading-[1.08]">
          Smarter Flights.
          <br />
          <span className="bg-gradient-to-r from-sky-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent">
            Smarter Prices.
          </span>
        </h1>
        <p className="mt-6 text-base sm:text-xl text-slate-300/90 max-w-2xl mx-auto font-normal leading-relaxed">
          AI-powered airfare price prediction and explainable flight intelligence. Discover real fare dynamics, feature attributions, and optimal travel timing.
        </p>
      </motion.div>

      {/* Interactive Aviation Route Graphic */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.3 }}
        className="w-full max-w-3xl my-10 relative px-4"
      >
        <div className="glass-panel p-6 sm:p-8 rounded-2xl relative overflow-hidden shadow-2xl border border-white/10">
          <div className="flex items-center justify-between relative z-10">
            {/* Origin */}
            <div className="flex flex-col items-start">
              <span className="text-3xl sm:text-4xl font-extrabold tracking-wider text-white">DEL</span>
              <span className="text-xs sm:text-sm text-slate-400 font-medium">New Delhi (Indira Gandhi Int&apos;l)</span>
              <span className="text-[11px] text-sky-400 mt-0.5 font-mono">Origin Hub</span>
            </div>

            {/* Flight Path Graphic */}
            <div className="flex-1 mx-4 sm:mx-8 relative flex flex-col items-center">
              <div className="w-full relative flex items-center justify-center">
                <svg className="w-full h-12 overflow-visible" viewBox="0 0 400 40">
                  {/* Base Route Arc Line */}
                  <path
                    d="M 10 30 Q 200 -5 390 30"
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.15)"
                    strokeWidth="2"
                  />
                  {/* Animated Dashed Arc Line */}
                  <path
                    d="M 10 30 Q 200 -5 390 30"
                    fill="none"
                    stroke="#38bdf8"
                    strokeWidth="2.5"
                    className="animate-flight-dash"
                  />
                </svg>

                {/* Aircraft floating near midpoint */}
                <motion.div
                  animate={{
                    x: [-12, 12, -12],
                    y: [-4, 4, -4],
                    rotate: [10, 16, 10],
                  }}
                  transition={{
                    duration: 5,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="absolute -top-1 bg-sky-500 text-white p-2 rounded-full shadow-[0_0_20px_#38bdf8]"
                >
                  <Plane className="w-5 h-5 -rotate-45" />
                </motion.div>
              </div>

              <div className="flex items-center gap-2 mt-3 text-xs text-slate-400">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                <span className="font-mono text-slate-300">Non-Stop • 2h 15m • High Frequency Route</span>
              </div>
            </div>

            {/* Destination */}
            <div className="flex flex-col items-end">
              <span className="text-3xl sm:text-4xl font-extrabold tracking-wider text-white">BOM</span>
              <span className="text-xs sm:text-sm text-slate-400 font-medium">Mumbai (Chhatrapati Shivaji)</span>
              <span className="text-[11px] text-sky-400 mt-0.5 font-mono">Metro Hub</span>
            </div>
          </div>

          {/* Micro badges below flight banner */}
          <div className="mt-6 pt-5 border-t border-white/5 grid grid-cols-3 gap-2 text-center">
            <div className="flex flex-col items-center">
              <span className="text-xs text-slate-400">Model Verification</span>
              <span className="text-xs sm:text-sm font-semibold text-slate-200 mt-0.5">MAE ±₹640.33</span>
            </div>
            <div className="flex flex-col items-center border-x border-white/5">
              <span className="text-xs text-slate-400">Dataset Coverage</span>
              <span className="text-xs sm:text-sm font-semibold text-slate-200 mt-0.5">10,462 Historical Flights</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-xs text-slate-400">Explainability</span>
              <span className="text-xs sm:text-sm font-semibold text-emerald-400 mt-0.5">100% Tree SHAP Additive</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto"
      >
        <a
          href="#predict"
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white font-semibold text-base shadow-[0_4px_25px_rgba(2,132,199,0.4)] transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
        >
          <Plane className="w-5 h-5 -rotate-45" />
          <span>Predict Flight Fare</span>
        </a>

        <a
          href="#analytics"
          className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 rounded-xl glass-panel hover:bg-slate-800/80 text-slate-200 font-semibold text-base transition-all duration-200 hover:border-sky-400/40 hover:scale-[1.02] active:scale-[0.98]"
        >
          <TrendingUp className="w-5 h-5 text-sky-400" />
          <span>Explore Market Analytics</span>
        </a>
      </motion.div>

      {/* Trust Badges */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.6 }}
        className="mt-14 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-400"
      >
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>Verified Holdout R² 0.9019</span>
        </div>
        <span className="text-slate-600">•</span>
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-sky-400" />
          <span>5 Source Cities & 6 Destination Hubs</span>
        </div>
        <span className="text-slate-600">•</span>
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-indigo-400" />
          <span>Local Tree SHAP Explanations</span>
        </div>
      </motion.div>
    </section>
  );
};
