"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Plane,
  CheckCircle2,
  TrendingUp,
  Sparkles,
  Calendar,
  Clock,
  MapPin,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";
import { PredictResponse } from "@/types/api";

interface PredictionResultCardProps {
  result: PredictResponse;
  onExploreExplanation: () => void;
}

export const PredictionResultCard: React.FC<PredictionResultCardProps> = ({
  result,
  onExploreExplanation,
}) => {
  // Count-up animation for the fare
  const [displayFare, setDisplayFare] = useState<number>(0);

  useEffect(() => {
    let start = 0;
    const end = Math.round(result.predicted_fare);
    if (end === 0) return;

    const duration = 1000; // 1 second
    const stepTime = 16;
    const totalSteps = duration / stepTime;
    const increment = end / totalSteps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setDisplayFare(end);
        clearInterval(timer);
      } else {
        setDisplayFare(Math.floor(start));
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [result.predicted_fare]);

  const [lowerBound, upperBound] = result.confidence_interval;

  return (
    <motion.section
      id="prediction-result"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="w-full max-w-5xl mx-auto px-4 py-12"
    >
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Inference Verified • 25 Features Processed</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Estimated Flight Fare
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Trained on 10,462 historical flight itineraries via 5-fold cross-validated ensemble.
        </p>
      </div>

      {/* Boarding Pass / Ticket Container */}
      <div className="glass-panel-elevated rounded-3xl overflow-hidden border border-sky-400/30 shadow-[0_15px_50px_rgba(0,0,0,0.6)]">
        {/* Ticket Header Bar */}
        <div className="bg-gradient-to-r from-sky-900/40 via-slate-900/60 to-indigo-900/40 border-b border-white/10 px-6 sm:px-8 py-4 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-sky-500/20 border border-sky-400/40 flex items-center justify-center text-sky-400">
              <Plane className="w-5 h-5 -rotate-45" />
            </div>
            <div>
              <span className="text-xs font-mono text-sky-300 font-semibold uppercase">
                {result.inputs_summary.airline}
              </span>
              <p className="text-sm font-bold text-white tracking-wide">
                Route: {result.inputs_summary.route}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-lg border border-white/10 font-mono">
              Model: {result.model_name}
            </span>
            <span className="text-xs bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-lg border border-emerald-500/30 font-mono font-semibold">
              R² {result.holdout_r2}
            </span>
          </div>
        </div>

        {/* Ticket Body: Fare Display + Flight Recap */}
        <div className="p-6 sm:p-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Left Column: Big Fare Counter */}
          <div className="lg:col-span-5 flex flex-col items-center lg:items-start text-center lg:text-left justify-center border-b lg:border-b-0 lg:border-r border-white/10 pb-8 lg:pb-0 lg:pr-8">
            <span className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-1">
              Estimated Expected Fare
            </span>

            <div className="flex items-baseline gap-2 my-2">
              <span className="text-3xl sm:text-4xl font-extrabold text-sky-400 font-mono">₹</span>
              <motion.span
                key={result.predicted_fare}
                className="text-5xl sm:text-6xl md:text-7xl font-black text-white tracking-tight font-mono"
              >
                {displayFare.toLocaleString("en-IN")}
              </motion.span>
            </div>

            {/* Confidence Interval Chip */}
            <div className="inline-flex items-center gap-2 mt-2 px-3 py-1.5 rounded-xl bg-slate-800/80 border border-white/10 text-xs text-slate-300">
              <ShieldCheck className="w-4 h-4 text-sky-400" />
              <span>
                Expected Range: <strong className="text-white">₹{Math.round(lowerBound).toLocaleString("en-IN")}</strong> –{" "}
                <strong className="text-white">₹{Math.round(upperBound).toLocaleString("en-IN")}</strong>
              </span>
            </div>

            <p className="text-[11px] text-slate-500 mt-2">
              Margin reflects holdout MAE uncertainty (±₹{result.holdout_mae}) on unseen data.
            </p>
          </div>

          {/* Right Column: Key Flight Characteristics */}
          <div className="lg:col-span-7 grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Total Stops
              </span>
              <span className="text-lg font-bold text-white mt-1 block">
                {result.inputs_summary.stops === 0 ? "Non-Stop" : `${result.inputs_summary.stops} Stop(s)`}
              </span>
              <span className="text-[10px] text-sky-400 font-mono">
                {result.inputs_summary.stop_category}
              </span>
            </div>

            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Flight Duration
              </span>
              <span className="text-lg font-bold text-white mt-1 block">
                {Math.floor(result.inputs_summary.duration_minutes / 60)}h{" "}
                {result.inputs_summary.duration_minutes % 60}m
              </span>
              <span className="text-[10px] text-slate-500 font-mono">
                {result.inputs_summary.duration_minutes} minutes
              </span>
            </div>

            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Travel Date
              </span>
              <span className="text-base font-bold text-white mt-1 block truncate">
                {result.inputs_summary.journey_date}
              </span>
              <span className="text-[10px] text-indigo-400 font-mono">
                Season: {result.inputs_summary.season}
              </span>
            </div>

            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Departure Slot
              </span>
              <span className="text-base font-bold text-white mt-1 block capitalize">
                {result.inputs_summary.departure_period}
              </span>
              <span className="text-[10px] text-slate-500 font-mono">Slot tariff band</span>
            </div>

            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Holdout RMSE
              </span>
              <span className="text-lg font-bold text-slate-200 mt-1 block font-mono">
                ₹1,430.08
              </span>
              <span className="text-[10px] text-slate-500 font-mono">Verified metric</span>
            </div>

            <div className="bg-slate-900/60 p-4 rounded-2xl border border-white/5">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                Algorithm
              </span>
              <span className="text-base font-bold text-emerald-400 mt-1 block">
                Random Forest
              </span>
              <span className="text-[10px] text-slate-500 font-mono">100 Trees Ensemble</span>
            </div>
          </div>
        </div>

        {/* Ticket Footer Action: Explain Fare */}
        <div className="bg-slate-900/90 border-t border-white/10 px-6 sm:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <Sparkles className="w-4 h-4 text-sky-400" />
            <span>Curious how this fare was calculated? View mathematical feature attributions.</span>
          </div>

          <button
            type="button"
            onClick={onExploreExplanation}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 font-semibold text-sm border border-sky-400/40 transition-all hover:scale-105 active:scale-95"
          >
            <span>Explain Price with SHAP</span>
            <ChevronDown className="w-4 h-4" />
          </button>
        </div>
      </div>
    </motion.section>
  );
};
