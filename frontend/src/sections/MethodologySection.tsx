"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  BookOpen,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  ShieldCheck,
  Cpu,
  Layers,
  Database,
  Terminal,
} from "lucide-react";

export const MethodologySection: React.FC = () => {
  return (
    <section id="about" className="w-full max-w-6xl mx-auto px-4 py-20">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-800 border border-white/10 text-slate-300 text-xs font-semibold uppercase tracking-wider mb-2">
          <BookOpen className="w-3.5 h-3.5 text-sky-400" />
          <span>Scientific Methodology &amp; Engineering</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          System Architecture &amp; Methodology
        </h2>
        <p className="text-slate-400 text-sm mt-1 max-w-2xl mx-auto">
          An engineering breakdown of the Airlytics machine learning pipeline, validation protocol, and scientific disclosures.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Card 1: Problem Statement & Dataset */}
        <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/5 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-sky-500/10 border border-sky-400/30 flex items-center justify-center text-sky-400">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Problem Statement &amp; Dataset</h3>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            Airline ticket pricing in India exhibits severe non-linear behavior driven by carrier oligopolies, route congestion, and layover logistics. Airlytics utilizes a standardized corpus of <strong>10,462 verified flight itineraries</strong> spanning major domestic hubs (Delhi, Mumbai, Kolkata, Banglore, Chennai, Cochin, and Hyderabad).
          </p>
          <div className="pt-2 flex flex-wrap gap-2 text-xs">
            <span className="bg-slate-800 text-slate-300 px-3 py-1 rounded-lg border border-white/5">
              10,462 Cleaned Records
            </span>
            <span className="bg-slate-800 text-slate-300 px-3 py-1 rounded-lg border border-white/5">
              5 Origin Hubs
            </span>
            <span className="bg-slate-800 text-slate-300 px-3 py-1 rounded-lg border border-white/5">
              6 Destination Terminals
            </span>
          </div>
        </div>

        {/* Card 2: Feature Engineering & Preprocessing */}
        <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/5 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-indigo-500/10 border border-indigo-400/30 flex items-center justify-center text-indigo-400">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">25-Feature Engineering Schema</h3>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            Raw flight timestamps and text entries are algorithmically decomposed into 25 deterministic features:
          </p>
          <ul className="text-xs text-slate-400 space-y-1.5 list-disc pl-4">
            <li><strong>Cyclic Temporal Signals:</strong> Sine and cosine transformations of departure and arrival hour to reflect continuous daily circadian cycles.</li>
            <li><strong>Duration &amp; Stops:</strong> Absolute flight minutes and numerical layover segment quantification.</li>
            <li><strong>Categorical Routing:</strong> Target-encoded airline tariff tier, source/destination corridor vectors, and baggage policy flags.</li>
          </ul>
        </div>

        {/* Card 3: Quality Assurance & 93-Test Suite */}
        <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/5 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-emerald-500/10 border border-emerald-400/30 flex items-center justify-center text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Testing &amp; Regression Integrity</h3>
          </div>
          <p className="text-sm text-slate-300 leading-relaxed">
            Unlike prototypical machine learning scripts, Airlytics enforces a comprehensive test suite of <strong>93 automated pytest unit and regression suites</strong>:
          </p>
          <ul className="text-xs text-slate-400 space-y-1.5 list-disc pl-4">
            <li>Complete validation against data leakage across training/test splits.</li>
            <li>Invariance testing of model inference outputs for deterministic reproducibility.</li>
            <li>Tree SHAP exact additive balance checks ensuring feature attribution sum matches prediction minus baseline.</li>
          </ul>
        </div>

        {/* Card 4: Limitations & Future Scope (Crucial Disclosure) */}
        <div className="glass-panel-elevated p-6 sm:p-8 rounded-3xl border border-amber-500/30 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-400/30 flex items-center justify-center text-amber-400">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Limitations &amp; Scientific Disclosure</h3>
          </div>
          <div className="bg-amber-500/10 border border-amber-400/20 p-4 rounded-2xl text-xs text-amber-200 leading-relaxed">
            <strong>Booking Lead Time Disclosure:</strong> The primary dataset provides journey dates but does not record historical purchase timestamps (booking window lead time). In adherence to scientific integrity, Airlytics does not fabricate booking window inputs.
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            <strong>Future Scope:</strong> Integration of live NDC/GDS airline streaming APIs, real-time jet fuel price indices, and empirical lead-time tracking for multi-horizon dynamic curve estimation.
          </p>
        </div>
      </div>
    </section>
  );
};
