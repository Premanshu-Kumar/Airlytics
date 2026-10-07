"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Brain,
  CheckCircle2,
  Trophy,
  Activity,
  Layers,
  Cpu,
  GitBranch,
  ShieldAlert,
} from "lucide-react";
import { apiService } from "@/services/apiClient";
import { ModelEvaluationResponse } from "@/types/api";

export const ModelPerformanceSection: React.FC = () => {
  const [evalData, setEvalData] = useState<ModelEvaluationResponse | null>(null);

  useEffect(() => {
    async function loadEval() {
      try {
        const res = await apiService.getModelEvaluation();
        setEvalData(res);
      } catch (err) {
        console.error("Failed to load model evaluation:", err);
      }
    }
    loadEval();
  }, []);

  const models = evalData?.models || [
    {
      rank: 1,
      model_name: "Random Forest Regressor",
      cv_mae_mean: 680.12,
      cv_mae_std: 24.3,
      holdout_mae: 640.33,
      holdout_rmse: 1430.08,
      holdout_r2: 0.9019,
      is_selected: true,
    },
    {
      rank: 2,
      model_name: "XGBoost Regressor",
      cv_mae_mean: 795.4,
      cv_mae_std: 28.1,
      holdout_mae: 782.15,
      holdout_rmse: 1645.22,
      holdout_r2: 0.8714,
      is_selected: false,
    },
    {
      rank: 3,
      model_name: "Linear Regression (OLS)",
      cv_mae_mean: 1985.3,
      cv_mae_std: 42.6,
      holdout_mae: 1962.4,
      holdout_rmse: 2814.5,
      holdout_r2: 0.6128,
      is_selected: false,
    },
  ];

  return (
    <section id="model" className="w-full max-w-6xl mx-auto px-4 py-20">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-400/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <Brain className="w-3.5 h-3.5" />
          <span>Machine Learning Benchmark</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          The AI Behind Airlytics
        </h2>
        <p className="text-slate-400 text-sm mt-1 max-w-2xl mx-auto">
          Rigorous 5-fold cross-validation and holdout evaluation across candidate regression architectures.
        </p>
      </div>

      {/* Architecture Pipeline Flow */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 mb-12 shadow-xl">
        <span className="text-xs font-bold text-sky-400 uppercase tracking-widest block mb-6 text-center">
          End-to-End Machine Learning Architecture
        </span>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center">
          {/* Step 1 */}
          <div className="bg-slate-900/80 p-4 rounded-2xl border border-white/5 text-center flex flex-col items-center">
            <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-400/30 flex items-center justify-center text-sky-400 mb-3">
              <Layers className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-white uppercase">Raw Flight Data</span>
            <span className="text-[11px] text-slate-400 mt-1">10,462 Verified domestic routes</span>
          </div>

          {/* Arrow */}
          <div className="hidden md:flex justify-center text-sky-400 font-bold text-lg">→</div>

          {/* Step 2 */}
          <div className="bg-slate-900/80 p-4 rounded-2xl border border-white/5 text-center flex flex-col items-center">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-400/30 flex items-center justify-center text-indigo-400 mb-3">
              <GitBranch className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-white uppercase">25-Feature Schema</span>
            <span className="text-[11px] text-slate-400 mt-1">Cyclic temporal &amp; route encodings</span>
          </div>

          {/* Arrow */}
          <div className="hidden md:flex justify-center text-sky-400 font-bold text-lg">→</div>

          {/* Step 3 */}
          <div className="bg-slate-900/80 p-4 rounded-2xl border border-emerald-500/40 text-center flex flex-col items-center shadow-[0_0_20px_rgba(16,185,129,0.15)]">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-400/30 flex items-center justify-center text-emerald-400 mb-3">
              <Cpu className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-emerald-300 uppercase">Random Forest</span>
            <span className="text-[11px] text-slate-300 mt-1">Selected ensemble (R² 0.9019)</span>
          </div>
        </div>
      </div>

      {/* Model Benchmark Leaderboard Cards */}
      <div className="space-y-4">
        {models.map((model) => (
          <div
            key={model.model_name}
            className={`p-6 sm:p-8 rounded-3xl border transition-all ${
              model.is_selected
                ? "glass-panel-elevated border-emerald-500/40 shadow-[0_10px_35px_rgba(16,185,129,0.1)] relative overflow-hidden"
                : "glass-panel border-white/5 opacity-80 hover:opacity-100"
            }`}
          >
            {model.is_selected && (
              <div className="absolute top-0 right-0 bg-emerald-500 text-slate-950 font-bold text-[10px] tracking-wider uppercase px-4 py-1 rounded-bl-xl flex items-center gap-1 shadow-md">
                <Trophy className="w-3 h-3" />
                <span>Production Selected Champion</span>
              </div>
            )}

            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div className="flex items-center gap-3">
                  <span className="w-7 h-7 rounded-lg bg-slate-800 text-slate-300 font-mono text-xs flex items-center justify-center font-bold">
                    #{model.rank}
                  </span>
                  <h3 className="text-xl font-bold text-white">{model.model_name}</h3>
                  {model.is_selected && (
                    <span className="hidden sm:inline-flex items-center gap-1 text-xs text-emerald-400 font-semibold">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      Active Predictor
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-400 mt-1.5">
                  5-Fold CV MAE: ±₹{model.cv_mae_mean.toFixed(2)} (std: ±₹{model.cv_mae_std.toFixed(2)})
                </p>
              </div>

              {/* Metrics Grid */}
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="bg-slate-900/60 p-3 rounded-2xl border border-white/5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Holdout MAE
                  </span>
                  <span className="text-base sm:text-lg font-bold font-mono text-white mt-0.5 block">
                    ₹{model.holdout_mae.toFixed(2)}
                  </span>
                </div>

                <div className="bg-slate-900/60 p-3 rounded-2xl border border-white/5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Holdout RMSE
                  </span>
                  <span className="text-base sm:text-lg font-bold font-mono text-slate-300 mt-0.5 block">
                    ₹{model.holdout_rmse.toFixed(2)}
                  </span>
                </div>

                <div className="bg-slate-900/60 p-3 rounded-2xl border border-white/5">
                  <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider block">
                    Holdout R²
                  </span>
                  <span className="text-base sm:text-lg font-black font-mono text-emerald-400 mt-0.5 block">
                    {model.holdout_r2.toFixed(4)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
