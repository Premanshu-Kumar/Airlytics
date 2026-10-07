"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  BarChart3,
  Users,
  Compass,
  DollarSign,
  ArrowUpRight,
  ShieldCheck,
  Plane,
} from "lucide-react";
import { apiService } from "@/services/apiClient";
import { AnalyticsOverviewResponse } from "@/types/api";

export const PriceAnalyticsSection: React.FC = () => {
  const [data, setData] = useState<AnalyticsOverviewResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"airlines" | "stops">("airlines");

  useEffect(() => {
    async function loadAnalytics() {
      try {
        const res = await apiService.getAnalyticsOverview();
        setData(res);
      } catch (err) {
        console.error("Failed to load analytics:", err);
      } finally {
        setLoading(false);
      }
    }
    loadAnalytics();
  }, []);

  const maxAirlineFare = data
    ? Math.max(...data.airlines.map((a) => a.median_fare), 1)
    : 15000;

  const maxStopFare = data
    ? Math.max(...data.stops.map((s) => s.median_fare), 1)
    : 15000;

  return (
    <section id="analytics" className="w-full max-w-6xl mx-auto px-4 py-20">
      {/* Section Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-indigo-500/10 border border-indigo-400/20 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <BarChart3 className="w-3.5 h-3.5" />
          <span>Market Intelligence &amp; Empirical Data</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          Explore Flight Prices
        </h2>
        <p className="text-slate-400 text-sm mt-1 max-w-2xl mx-auto">
          Comprehensive market distribution across 10,462 verified flight itineraries in the Airlytics baseline dataset.
        </p>
      </div>

      {/* Top 4 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.05 }}
          className="glass-panel p-5 rounded-2xl border border-white/5"
        >
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Median Ticket Fare
          </span>
          <div className="flex items-baseline gap-1 mt-2">
            <span className="text-xl font-bold font-mono text-sky-400">₹</span>
            <span className="text-2xl sm:text-3xl font-black text-white font-mono">
              {data ? data.median_fare.toLocaleString("en-IN") : "8,366"}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Robust non-skewed central price</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="glass-panel p-5 rounded-2xl border border-white/5"
        >
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Mean Average Fare
          </span>
          <div className="flex items-baseline gap-1 mt-2">
            <span className="text-xl font-bold font-mono text-indigo-400">₹</span>
            <span className="text-2xl sm:text-3xl font-black text-white font-mono">
              {data ? Math.round(data.mean_fare).toLocaleString("en-IN") : "9,087"}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Dataset arithmetic average</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.15 }}
          className="glass-panel p-5 rounded-2xl border border-white/5"
        >
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Verified Flight Records
          </span>
          <div className="mt-2">
            <span className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">
              {data ? data.total_records.toLocaleString("en-IN") : "10,462"}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Cleaned &amp; validated flight samples</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="glass-panel p-5 rounded-2xl border border-white/5"
        >
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
            Observed Fare Spectrum
          </span>
          <div className="flex items-baseline gap-1 mt-2">
            <span className="text-sm font-mono text-slate-400">₹</span>
            <span className="text-xl sm:text-2xl font-black text-white font-mono">
              {data ? `${data.min_fare.toLocaleString("en-IN")} – ${data.max_fare.toLocaleString("en-IN")}` : "1,759 – 79,512"}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Economy promos to peak business</p>
        </motion.div>
      </div>

      {/* Main Analytics Panel */}
      <div className="glass-panel-elevated rounded-3xl p-6 sm:p-10 border border-white/10 shadow-2xl">
        {/* Toggle between Airline Comparison and Stops Analysis */}
        <div className="flex items-center justify-between border-b border-white/10 pb-5 mb-8">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setActiveTab("airlines")}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                activeTab === "airlines"
                  ? "bg-sky-500 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Airline Tariff Comparison
            </button>
            <button
              type="button"
              onClick={() => setActiveTab("stops")}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                activeTab === "stops"
                  ? "bg-sky-500 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Layover Stops vs. Median Fare
            </button>
          </div>

          <span className="text-xs text-slate-400 font-mono hidden sm:inline">
            Source: Cleaned Airfare Corpus
          </span>
        </div>

        {/* Tab 1: Airline Breakdown */}
        {activeTab === "airlines" && data && (
          <div className="space-y-4">
            <div className="grid grid-cols-12 text-xs font-semibold text-slate-400 uppercase tracking-wider pb-2 border-b border-white/5 px-3">
              <span className="col-span-4 sm:col-span-3">Airline Carrier</span>
              <span className="col-span-5 sm:col-span-6">Median Fare Distribution</span>
              <span className="col-span-3 sm:col-span-3 text-right">Flight Volume</span>
            </div>

            <div className="space-y-3">
              {data.airlines.map((carrier, idx) => {
                const barWidth = Math.min(100, (carrier.median_fare / maxAirlineFare) * 100);

                return (
                  <div
                    key={carrier.airline}
                    className="grid grid-cols-12 items-center bg-slate-900/40 hover:bg-slate-900/80 p-3.5 rounded-2xl border border-white/5 transition-all gap-2"
                  >
                    <div className="col-span-4 sm:col-span-3">
                      <span className="text-sm font-bold text-white block truncate">
                        {carrier.airline}
                      </span>
                    </div>

                    <div className="col-span-5 sm:col-span-6 flex items-center gap-3">
                      <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          whileInView={{ width: `${barWidth}%` }}
                          viewport={{ once: true }}
                          transition={{ duration: 0.6, delay: idx * 0.05 }}
                          className="h-full rounded-full bg-gradient-to-r from-sky-500 to-indigo-500"
                        />
                      </div>
                      <span className="text-xs sm:text-sm font-mono font-bold text-sky-300 shrink-0">
                        ₹{carrier.median_fare.toLocaleString("en-IN")}
                      </span>
                    </div>

                    <div className="col-span-3 sm:col-span-3 text-right">
                      <span className="text-xs font-mono text-slate-300 bg-slate-800 px-2 py-1 rounded-md border border-white/5">
                        {carrier.count.toLocaleString("en-IN")} flights
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Tab 2: Stops Breakdown */}
        {activeTab === "stops" && data && (
          <div className="space-y-4">
            <p className="text-sm text-slate-300 mb-4">
              Direct evidence of pricing escalation caused by additional aircraft legs, airport transit handling, and duration expansion.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
              {data.stops.map((stopItem) => (
                <div
                  key={stopItem.stops}
                  className="bg-slate-900/60 p-5 rounded-2xl border border-white/5 flex flex-col justify-between"
                >
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      {stopItem.stops === 0 ? "Non-Stop" : `${stopItem.stops} Layover Stop(s)`}
                    </span>
                    <div className="flex items-baseline gap-1 mt-2">
                      <span className="text-sm font-mono text-sky-400">₹</span>
                      <span className="text-2xl font-black text-white font-mono">
                        {stopItem.median_fare.toLocaleString("en-IN")}
                      </span>
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
                    <span>Flights in dataset:</span>
                    <span className="font-mono text-slate-200 font-semibold">{stopItem.count}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
};
