"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Compass, Plane, ArrowRight, Clock, ShieldCheck, MapPin } from "lucide-react";

interface Corridor {
  id: string;
  source: string;
  sourceCode: string;
  destination: string;
  destCode: string;
  medianPrice: number;
  minPrice: number;
  maxPrice: number;
  durationAvg: string;
  routes: string[];
  airlines: string[];
}

const CORRIDORS: Corridor[] = [
  {
    id: "del-cok",
    source: "Delhi",
    sourceCode: "DEL",
    destination: "Cochin",
    destCode: "COK",
    medianPrice: 10262,
    minPrice: 4226,
    maxPrice: 31825,
    durationAvg: "9h 30m",
    routes: ["DEL → BOM → COK", "DEL → BLR → COK", "DEL → HYD → COK"],
    airlines: ["IndiGo", "Air India", "Jet Airways", "SpiceJet"],
  },
  {
    id: "del-bom",
    source: "Delhi",
    sourceCode: "DEL",
    destination: "Mumbai",
    destCode: "BOM",
    medianPrice: 6213,
    minPrice: 3859,
    maxPrice: 24045,
    durationAvg: "2h 15m",
    routes: ["DEL → BOM (Non-stop)"],
    airlines: ["IndiGo", "SpiceJet", "Air India", "Jet Airways"],
  },
  {
    id: "ccu-blr",
    source: "Kolkata",
    sourceCode: "CCU",
    destination: "Banglore",
    destCode: "BLR",
    medianPrice: 9134,
    minPrice: 4174,
    maxPrice: 26890,
    durationAvg: "7h 45m",
    routes: ["CCU → BOM → BLR", "CCU → DEL → BLR", "CCU → BLR (Non-stop)"],
    airlines: ["IndiGo", "Air India", "Jet Airways"],
  },
  {
    id: "blr-del",
    source: "Banglore",
    sourceCode: "BLR",
    destination: "Delhi",
    destCode: "DEL",
    medianPrice: 4823,
    minPrice: 3359,
    maxPrice: 19828,
    durationAvg: "2h 50m",
    routes: ["BLR → DEL (Non-stop)"],
    airlines: ["Air Asia", "IndiGo", "SpiceJet", "Vistara"],
  },
  {
    id: "maa-ccu",
    source: "Chennai",
    sourceCode: "MAA",
    destination: "Kolkata",
    destCode: "CCU",
    medianPrice: 3850,
    minPrice: 3145,
    maxPrice: 13496,
    durationAvg: "2h 20m",
    routes: ["MAA → CCU (Non-stop)"],
    airlines: ["IndiGo", "SpiceJet", "Air India"],
  },
];

export const RouteExplorerSection: React.FC = () => {
  const [selectedCorridor, setSelectedCorridor] = useState<Corridor>(CORRIDORS[0]);

  return (
    <section id="routes" className="w-full max-w-6xl mx-auto px-4 py-20">
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-400/20 text-cyan-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <Compass className="w-3.5 h-3.5" />
          <span>Interactive Route Explorer</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Major Flight Corridors
        </h2>
        <p className="text-slate-400 text-sm mt-1 max-w-2xl mx-auto">
          Explore benchmark pricing profiles and transit variations for primary domestic aviation corridors.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Corridor Selector List */}
        <div className="lg:col-span-4 space-y-3">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-2 px-1">
            Select Aviation Corridor
          </span>
          {CORRIDORS.map((c) => {
            const isSelected = selectedCorridor.id === c.id;
            return (
              <button
                key={c.id}
                type="button"
                onClick={() => setSelectedCorridor(c)}
                className={`w-full p-4 rounded-2xl border text-left transition-all flex items-center justify-between ${
                  isSelected
                    ? "bg-slate-800/90 border-sky-400 shadow-[0_0_20px_rgba(56,189,248,0.15)]"
                    : "glass-panel border-white/5 hover:border-white/20 hover:bg-slate-900/60"
                }`}
              >
                <div>
                  <div className="flex items-center gap-2 font-bold text-white text-base">
                    <span>{c.sourceCode}</span>
                    <ArrowRight className="w-4 h-4 text-sky-400" />
                    <span>{c.destCode}</span>
                  </div>
                  <span className="text-xs text-slate-400 mt-0.5 block">
                    {c.source} → {c.destination}
                  </span>
                </div>

                <div className="text-right">
                  <span className="text-xs font-mono text-slate-400 block">Median</span>
                  <span className="text-sm font-bold font-mono text-sky-300">
                    ₹{c.medianPrice.toLocaleString("en-IN")}
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Corridor Deep Dive Card */}
        <div className="lg:col-span-8 glass-panel-elevated rounded-3xl p-6 sm:p-8 border border-white/10 shadow-2xl">
          {/* Corridor Banner Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-white/10 gap-4">
            <div className="flex items-center gap-4">
              <div className="flex flex-col items-center">
                <span className="text-2xl sm:text-3xl font-black text-white font-mono">
                  {selectedCorridor.sourceCode}
                </span>
                <span className="text-xs text-slate-400">{selectedCorridor.source}</span>
              </div>

              <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-300 text-xs font-mono">
                <Plane className="w-3.5 h-3.5 -rotate-45" />
                <span>Typical: {selectedCorridor.durationAvg}</span>
              </div>

              <div className="flex flex-col items-center">
                <span className="text-2xl sm:text-3xl font-black text-white font-mono">
                  {selectedCorridor.destCode}
                </span>
                <span className="text-xs text-slate-400">{selectedCorridor.destination}</span>
              </div>
            </div>

            <div className="text-left sm:text-right">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
                Historical Fare Window
              </span>
              <span className="text-lg font-bold font-mono text-emerald-400">
                ₹{selectedCorridor.minPrice.toLocaleString("en-IN")} – ₹{selectedCorridor.maxPrice.toLocaleString("en-IN")}
              </span>
            </div>
          </div>

          {/* Available Routing Patterns in dataset */}
          <div className="mt-6">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-3">
              Identified Dataset Flight Patterns
            </span>
            <div className="flex flex-wrap gap-2">
              {selectedCorridor.routes.map((rt) => (
                <div
                  key={rt}
                  className="px-3.5 py-2 rounded-xl bg-slate-900 border border-white/10 text-xs font-mono text-slate-200 flex items-center gap-2"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-sky-400" />
                  <span>{rt}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Operating Airlines */}
          <div className="mt-6">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-3">
              Frequent Operating Airlines
            </span>
            <div className="flex flex-wrap gap-2">
              {selectedCorridor.airlines.map((air) => (
                <span
                  key={air}
                  className="px-3 py-1.5 rounded-lg bg-slate-800/80 text-xs font-medium text-slate-300 border border-white/5"
                >
                  {air}
                </span>
              ))}
            </div>
          </div>

          {/* Callout */}
          <div className="mt-8 p-4 rounded-2xl bg-sky-500/10 border border-sky-400/20 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-5 h-5 text-sky-400 shrink-0" />
              <span className="text-xs sm:text-sm text-slate-300">
                Ready to estimate a specific flight on this route?
              </span>
            </div>
            <a
              href="#predict"
              className="px-4 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold transition-all shrink-0 shadow-md"
            >
              Configure in Predictor →
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};
