"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Sparkles,
  TrendingUp,
  TrendingDown,
  Info,
  CheckCircle2,
  HelpCircle,
  Layers,
  ArrowRight,
} from "lucide-react";
import { ExplainResponse, ShapContribution } from "@/types/api";

interface WhyThisPriceSectionProps {
  explanation: ExplainResponse | null;
  predictedFare: number;
}

export const WhyThisPriceSection: React.FC<WhyThisPriceSectionProps> = ({
  explanation,
  predictedFare,
}) => {
  const [showAllFeatures, setShowAllFeatures] = useState(false);

  if (!explanation) {
    return (
      <section id="shap-explanation" className="w-full max-w-5xl mx-auto px-4 py-16">
        <div className="glass-panel rounded-3xl p-8 text-center border border-white/10">
          <Sparkles className="w-8 h-8 text-sky-400 mx-auto mb-3 animate-pulse" />
          <h3 className="text-xl font-bold text-white">Why This Price? (SHAP Explainability)</h3>
          <p className="text-sm text-slate-400 mt-2 max-w-md mx-auto">
            Configure your flight parameters above and click <strong>Predict Flight Fare</strong> to generate a complete mathematical breakdown of pricing factors.
          </p>
        </div>
      </section>
    );
  }

  const contributorsToDisplay = showAllFeatures
    ? explanation.all_contributors
    : explanation.top_contributors;

  // Maximum absolute contribution for proportional bar widths
  const maxAbsContribution = Math.max(
    ...contributorsToDisplay.map((c) => Math.abs(c.contribution)),
    100
  );

  return (
    <motion.section
      id="shap-explanation"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
      className="w-full max-w-5xl mx-auto px-4 py-16"
    >
      {/* Section Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <Layers className="w-3.5 h-3.5" />
          <span>Local Explainable AI (XAI)</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Why This Price?
        </h2>
        <p className="text-slate-400 text-sm mt-1 max-w-2xl mx-auto">
          Local Tree-SHAP attributions reveal the precise price addition or discount imparted by every flight characteristic.
        </p>
      </div>

      <div className="glass-panel-elevated rounded-3xl p-6 sm:p-10 border border-sky-400/20 shadow-2xl space-y-8">
        {/* SHAP Additivity Equation Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-center bg-slate-900/70 p-5 rounded-2xl border border-white/5">
          {/* Baseline */}
          <div className="text-center md:text-left">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Model Base Expected Fare
            </span>
            <div className="flex items-baseline gap-1 mt-1 justify-center md:justify-start">
              <span className="text-sm font-mono text-slate-400">₹</span>
              <span className="text-2xl font-bold text-slate-200 font-mono">
                {Math.round(explanation.model_baseline).toLocaleString("en-IN")}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">Average dataset flight cost</p>
          </div>

          {/* Net Adjustment */}
          <div className="text-center border-y md:border-y-0 md:border-x border-white/10 py-3 md:py-0">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Net SHAP Adjustment
            </span>
            <div className="flex items-center justify-center gap-1.5 mt-1">
              {explanation.net_shap_adjustment >= 0 ? (
                <TrendingUp className="w-5 h-5 text-rose-400" />
              ) : (
                <TrendingDown className="w-5 h-5 text-emerald-400" />
              )}
              <span
                className={`text-2xl font-bold font-mono ${
                  explanation.net_shap_adjustment >= 0 ? "text-rose-400" : "text-emerald-400"
                }`}
              >
                {explanation.net_shap_adjustment >= 0 ? "+" : ""}₹
                {Math.round(explanation.net_shap_adjustment).toLocaleString("en-IN")}
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-0.5">Sum of all feature pushes</p>
          </div>

          {/* Final Predicted Fare */}
          <div className="text-center md:text-right">
            <span className="text-[11px] font-bold text-sky-400 uppercase tracking-wider block">
              Final Predicted Fare
            </span>
            <div className="flex items-baseline gap-1 mt-1 justify-center md:justify-end">
              <span className="text-sm font-mono text-sky-400 font-bold">₹</span>
              <span className="text-2xl font-black text-white font-mono">
                {Math.round(predictedFare).toLocaleString("en-IN")}
              </span>
            </div>
            <div className="inline-flex items-center gap-1 text-[11px] text-emerald-400 mt-0.5 justify-center md:justify-end">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Exact Additive Balance Verified</span>
            </div>
          </div>
        </div>

        {/* Plain English AI Synthesis Box */}
        <div className="bg-sky-500/10 border border-sky-400/25 p-5 rounded-2xl flex items-start gap-3.5">
          <div className="p-2 rounded-xl bg-sky-500/20 text-sky-400 shrink-0 mt-0.5">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs font-bold text-sky-300 uppercase tracking-wider block">
              AI Mathematical Takeaway
            </span>
            <p className="text-sm sm:text-base text-slate-200 mt-1 font-medium leading-relaxed">
              {explanation.summary_sentence}
            </p>
          </div>
        </div>

        {/* Feature Contribution Bars */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <span>Primary Factor Impact Breakdown</span>
              <span className="text-xs font-normal text-slate-400">
                ({contributorsToDisplay.length} features analyzed)
              </span>
            </h3>

            <div className="flex items-center gap-4 text-xs font-medium">
              <span className="flex items-center gap-1.5 text-rose-400">
                <span className="w-2.5 h-2.5 rounded-sm bg-rose-500" />
                Surcharge Factor (+)
              </span>
              <span className="flex items-center gap-1.5 text-emerald-400">
                <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
                Discount Factor (−)
              </span>
            </div>
          </div>

          <div className="space-y-3">
            {contributorsToDisplay.map((item, idx) => {
              const isPositive = item.contribution >= 0;
              const barPercentage = Math.min(
                100,
                Math.max(8, (Math.abs(item.contribution) / maxAbsContribution) * 100)
              );

              return (
                <div
                  key={`${item.feature}-${idx}`}
                  className="bg-slate-900/50 hover:bg-slate-900/80 p-4 rounded-2xl border border-white/5 transition-all"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-white">{item.feature}</span>
                      <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded-md border border-white/5">
                        {item.value}
                      </span>
                      <span
                        className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                          item.impact_level === "High Impact"
                            ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                            : "bg-slate-800 text-slate-400"
                        }`}
                      >
                        {item.impact_level}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 sm:text-right">
                      <span
                        className={`text-sm font-bold font-mono ${
                          isPositive ? "text-rose-400" : "text-emerald-400"
                        }`}
                      >
                        {isPositive ? "+" : "−"}₹{Math.round(Math.abs(item.contribution)).toLocaleString("en-IN")}
                      </span>
                      <span className="text-[11px] text-slate-500 uppercase font-mono">
                        ({item.direction})
                      </span>
                    </div>
                  </div>

                  {/* Impact Bar */}
                  <div className="w-full bg-slate-800/80 h-2.5 rounded-full overflow-hidden relative">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${barPercentage}%` }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.6, delay: idx * 0.05 }}
                      className={`h-full rounded-full ${
                        isPositive
                          ? "bg-gradient-to-r from-rose-500 to-amber-500 shadow-[0_0_10px_rgba(244,63,94,0.4)]"
                          : "bg-gradient-to-r from-emerald-500 to-teal-400 shadow-[0_0_10px_rgba(16,185,129,0.4)]"
                      }`}
                    />
                  </div>

                  {/* Plain English explanation for this feature */}
                  <p className="text-xs text-slate-400 mt-2 italic">
                    &ldquo;{item.plain_english}&rdquo;
                  </p>
                </div>
              );
            })}
          </div>

          {/* Toggle All Features */}
          <div className="text-center pt-2">
            <button
              type="button"
              onClick={() => setShowAllFeatures(!showAllFeatures)}
              className="text-xs font-semibold text-sky-400 hover:text-sky-300 underline underline-offset-4 transition-colors"
            >
              {showAllFeatures ? "Collapse to Top Key Contributors" : "Show All Calculated Feature Drivers"}
            </button>
          </div>
        </div>
      </div>
    </motion.section>
  );
};
