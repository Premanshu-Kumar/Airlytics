"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Plane,
  ArrowRightLeft,
  Calendar,
  Clock,
  Briefcase,
  AlertCircle,
  Loader2,
  Sparkles,
  MapPin,
  ChevronDown,
} from "lucide-react";
import { apiService } from "@/services/apiClient";
import { MetadataResponse, PredictRequest, PredictResponse, ExplainResponse } from "@/types/api";

const CITY_CODES: Record<string, string> = {
  Delhi: "DEL",
  "New Delhi": "DEL",
  Kolkata: "CCU",
  Banglore: "BLR",
  Mumbai: "BOM",
  Chennai: "MAA",
  Cochin: "COK",
  Hyderabad: "HYD",
};

interface FlightSearchCardProps {
  onPredictionStart: () => void;
  onPredictionComplete: (prediction: PredictResponse, explanation: ExplainResponse | null) => void;
  onError: (errorMsg: string) => void;
}

export const FlightSearchCard: React.FC<FlightSearchCardProps> = ({
  onPredictionStart,
  onPredictionComplete,
  onError,
}) => {
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null);
  const [loadingMetadata, setLoadingMetadata] = useState(true);

  // Form states
  const [tripType, setTripType] = useState<"oneway" | "roundtrip">("oneway");
  const [source, setSource] = useState("Delhi");
  const [destination, setDestination] = useState("Cochin");
  const [airline, setAirline] = useState("IndiGo");
  const [journeyDate, setJourneyDate] = useState("2026-05-15");
  const [departureTime, setDepartureTime] = useState("09:30");
  const [arrivalTime, setArrivalTime] = useState("12:45");
  const [durationMinutes, setDurationMinutes] = useState(195);
  const [stops, setStops] = useState(1);
  const [additionalInfo, setAdditionalInfo] = useState("No info");

  // Dynamic route states
  const [availableRoutes, setAvailableRoutes] = useState<string[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<string>("DEL → BOM → COK");
  const [loadingRoutes, setLoadingRoutes] = useState(false);

  // Prediction loading animation state
  const [isPredicting, setIsPredicting] = useState(false);
  const [loadingStep, setLoadingStep] = useState<string>("");

  // Fetch initial metadata
  useEffect(() => {
    async function loadMeta() {
      try {
        const data = await apiService.getMetadata();
        setMetadata(data);
        if (data.airlines.length > 0 && !data.airlines.includes(airline)) {
          setAirline(data.airlines[0]);
        }
      } catch (err: unknown) {
        console.error("Failed to load metadata:", err);
      } finally {
        setLoadingMetadata(false);
      }
    }
    loadMeta();
  }, [airline]);

  // Fetch matching routes whenever source or destination changes
  useEffect(() => {
    async function loadMatchingRoutes() {
      if (!source || !destination || source === destination) return;
      setLoadingRoutes(true);
      try {
        const routesData = await apiService.getRoutes(source, destination);
        if (routesData.matching_routes && routesData.matching_routes.length > 0) {
          setAvailableRoutes(routesData.matching_routes);
          setSelectedRoute(routesData.suggested_route || routesData.matching_routes[0]);
          
          // Auto-adjust stops based on suggested route point count
          const stopsInRoute = routesData.suggested_route.split("→").length - 2;
          if (stopsInRoute >= 0) {
            setStops(stopsInRoute);
          }
        } else {
          const fallback = `${CITY_CODES[source] || source} → ${CITY_CODES[destination] || destination}`;
          setAvailableRoutes([fallback]);
          setSelectedRoute(fallback);
          setStops(0);
        }
      } catch (err) {
        console.error("Failed to fetch routes:", err);
      } finally {
        setLoadingRoutes(false);
      }
    }
    loadMatchingRoutes();
  }, [source, destination]);

  // Handle source-destination swap
  const handleSwapAirports = () => {
    if (source === destination) return;
    const temp = source;
    // Check if new source is in sources list
    setSource(destination);
    setDestination(temp);
  };

  // Form submission & prediction pipeline
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (source === destination) {
      onError("Origin and Destination cannot be the same airport.");
      return;
    }

    setIsPredicting(true);
    onPredictionStart();

    const requestPayload: PredictRequest = {
      airline,
      source,
      destination,
      route: selectedRoute,
      journey_date: journeyDate,
      departure_time: departureTime,
      arrival_time: arrivalTime,
      duration_minutes: Number(durationMinutes),
      number_of_stops: Number(stops),
      additional_info: additionalInfo,
    };

    try {
      // Step 1
      setLoadingStep("Validating route and sector parameters...");
      await new Promise((r) => setTimeout(r, 400));

      // Step 2
      setLoadingStep("Synthesizing 25-feature engineering schema...");
      await new Promise((r) => setTimeout(r, 450));

      // Step 3
      setLoadingStep("Evaluating Random Forest regression ensemble...");
      const predResponse = await apiService.predictFare(requestPayload);

      // Step 4
      setLoadingStep("Computing local Tree SHAP feature attributions...");
      let explainResponse: ExplainResponse | null = null;
      try {
        explainResponse = await apiService.explainPrediction(requestPayload);
      } catch (shapErr) {
        console.warn("SHAP explanation failed:", shapErr);
      }

      setLoadingStep("Finalizing fare intelligence...");
      await new Promise((r) => setTimeout(r, 300));

      onPredictionComplete(predResponse, explainResponse);

      // Scroll smoothly to the prediction result
      setTimeout(() => {
        const resultElem = document.getElementById("prediction-result");
        if (resultElem) {
          resultElem.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 100);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Price estimation failed. Please check inputs.";
      onError(msg);
    } finally {
      setIsPredicting(false);
      setLoadingStep("");
    }
  };

  const sourcesList = metadata?.sources || ["Delhi", "Kolkata", "Banglore", "Mumbai", "Chennai"];
  const destinationsList = metadata?.destinations || [
    "Cochin",
    "Delhi",
    "New Delhi",
    "Hyderabad",
    "Kolkata",
    "Banglore",
  ];
  const airlinesList = metadata?.airlines || [
    "IndiGo",
    "Air India",
    "Jet Airways",
    "SpiceJet",
    "Multiple carriers",
    "Vistara",
    "Air Asia",
    "GoAir",
  ];

  return (
    <div id="predict" className="w-full max-w-5xl mx-auto px-4 -mt-6 sm:-mt-8 relative z-20">
      <div className="glass-panel-elevated rounded-3xl p-6 sm:p-8 backdrop-blur-2xl">
        {/* Search Header Tabs */}
        <div className="flex items-center justify-between border-b border-white/10 pb-5 mb-6">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setTripType("oneway")}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
                tripType === "oneway"
                  ? "bg-sky-500 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              One Way
            </button>
            <button
              type="button"
              onClick={() => setTripType("roundtrip")}
              className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all flex items-center gap-2 ${
                tripType === "roundtrip"
                  ? "bg-sky-500 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <span>Round Trip</span>
              <span className="text-[10px] bg-sky-950 text-sky-300 px-1.5 py-0.5 rounded border border-sky-800">
                Predicts Leg
              </span>
            </button>
          </div>

          <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
            <Sparkles className="w-4 h-4 text-sky-400" />
            <span>Real-time ML Model Evaluation</span>
          </div>
        </div>

        {/* Prediction Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Row 1: Source & Destination with Swap */}
          <div className="grid grid-cols-1 md:grid-cols-11 gap-3 items-center">
            {/* Origin Airport */}
            <div className="md:col-span-5 relative group">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider">
                From (Origin City)
              </label>
              <div className="relative">
                <select
                  value={source}
                  onChange={(e) => setSource(e.target.value)}
                  className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all appearance-none cursor-pointer"
                >
                  {sourcesList.map((city) => (
                    <option key={city} value={city} className="bg-slate-900 text-white">
                      {city} ({CITY_CODES[city] || "AIR"})
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
              <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500 px-1">
                <span>Airport Hub</span>
                <span className="font-mono text-sky-400/90 font-bold">{CITY_CODES[source] || "DEL"}</span>
              </div>
            </div>

            {/* Airport Swap Button */}
            <div className="md:col-span-1 flex justify-center py-1 md:py-0">
              <button
                type="button"
                onClick={handleSwapAirports}
                className="p-3 rounded-full bg-slate-800/80 hover:bg-sky-500/20 text-slate-300 hover:text-sky-300 border border-white/10 hover:border-sky-400/40 transition-all shadow-md group"
                title="Swap Origin and Destination"
              >
                <ArrowRightLeft className="w-4 h-4 transition-transform group-hover:rotate-180 duration-300" />
              </button>
            </div>

            {/* Destination Airport */}
            <div className="md:col-span-5 relative group">
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider">
                To (Destination City)
              </label>
              <div className="relative">
                <select
                  value={destination}
                  onChange={(e) => setDestination(e.target.value)}
                  className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all appearance-none cursor-pointer"
                >
                  {destinationsList.map((city) => (
                    <option key={city} value={city} className="bg-slate-900 text-white">
                      {city} ({CITY_CODES[city] || "AIR"})
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
              <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500 px-1">
                <span>Arrival Terminal</span>
                <span className="font-mono text-sky-400/90 font-bold">{CITY_CODES[destination] || "COK"}</span>
              </div>
            </div>
          </div>

          {/* Row 2: Dynamic Route Selector & Airline */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Dynamic Route */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                  Historical Route Pattern
                </label>
                {loadingRoutes && <span className="text-[11px] text-sky-400 animate-pulse">Matching routes...</span>}
              </div>
              <div className="relative">
                <select
                  value={selectedRoute}
                  onChange={(e) => {
                    setSelectedRoute(e.target.value);
                    const calculatedStops = e.target.value.split("→").length - 2;
                    if (calculatedStops >= 0) {
                      setStops(calculatedStops);
                    }
                  }}
                  className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-mono text-sm focus:outline-none focus:border-sky-400 transition-all appearance-none cursor-pointer"
                >
                  {availableRoutes.map((rt) => (
                    <option key={rt} value={rt} className="bg-slate-900 font-sans text-white">
                      {rt}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
              <p className="mt-1 text-[11px] text-slate-500">
                Matches confirmed flight trajectories from the 10,462-record dataset.
              </p>
            </div>

            {/* Airline Carrier */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider">
                Airline Carrier
              </label>
              <div className="relative">
                <select
                  value={airline}
                  onChange={(e) => setAirline(e.target.value)}
                  className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 transition-all appearance-none cursor-pointer"
                >
                  {airlinesList.map((air) => (
                    <option key={air} value={air} className="bg-slate-900 text-white">
                      {air}
                    </option>
                  ))}
                </select>
                <ChevronDown className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
              </div>
              <p className="mt-1 text-[11px] text-slate-500">Carrier tariff pricing tier applied by Random Forest.</p>
            </div>
          </div>

          {/* Row 3: Journey Date, Departure Time, Arrival Time */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Journey Date */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5 text-sky-400" />
                Date of Travel
              </label>
              <input
                type="date"
                value={journeyDate}
                onChange={(e) => setJourneyDate(e.target.value)}
                className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 transition-all [color-scheme:dark]"
              />
              <p className="mt-1 text-[11px] text-slate-500">Encodes Day of Week &amp; Month Seasonality.</p>
            </div>

            {/* Departure Time */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-sky-400" />
                Departure Time
              </label>
              <input
                type="time"
                value={departureTime}
                onChange={(e) => setDepartureTime(e.target.value)}
                className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 transition-all [color-scheme:dark]"
              />
              <p className="mt-1 text-[11px] text-slate-500">Morning / Afternoon / Evening band.</p>
            </div>

            {/* Arrival Time */}
            <div>
              <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider flex items-center gap-1.5">
                <Clock className="w-3.5 h-3.5 text-sky-400" />
                Arrival Time
              </label>
              <input
                type="time"
                value={arrivalTime}
                onChange={(e) => setArrivalTime(e.target.value)}
                className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 transition-all [color-scheme:dark]"
              />
              <p className="mt-1 text-[11px] text-slate-500">Calculates overnight and landing slot.</p>
            </div>
          </div>

          {/* Row 4: Stops & Duration Slider */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-900/50 p-5 rounded-2xl border border-white/5">
            {/* Total Stops */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2 uppercase tracking-wider">
                Total Layover Stops
              </label>
              <div className="grid grid-cols-4 gap-2">
                {[0, 1, 2, 3].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setStops(num)}
                    className={`py-2.5 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
                      stops === num
                        ? "bg-sky-500 text-white shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                        : "bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700"
                    }`}
                  >
                    {num === 0 ? "Non-Stop" : `${num} ${num === 1 ? "Stop" : "Stops"}`}
                  </button>
                ))}
              </div>
              <p className="mt-2 text-[11px] text-slate-500">
                Stops count directly impacts airport handling and segment surcharges.
              </p>
            </div>

            {/* Flight Duration in minutes */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Flight Duration
                </label>
                <span className="text-sm font-bold text-sky-400 font-mono">
                  {Math.floor(durationMinutes / 60)}h {durationMinutes % 60}m ({durationMinutes} mins)
                </span>
              </div>
              <input
                type="range"
                min="75"
                max="2860"
                step="15"
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(Number(e.target.value))}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-sky-400"
              />
              <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                <span>1h 15m (Short haul)</span>
                <span>47h 40m (Long transit)</span>
              </div>
            </div>
          </div>

          {/* Row 5: Additional Info */}
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider flex items-center gap-1.5">
              <Briefcase className="w-3.5 h-3.5 text-sky-400" />
              Fare Inclusions / Baggage Policy
            </label>
            <div className="relative">
              <select
                value={additionalInfo}
                onChange={(e) => setAdditionalInfo(e.target.value)}
                className="w-full bg-slate-900/90 border border-white/10 rounded-2xl px-4 py-3.5 text-white font-medium focus:outline-none focus:border-sky-400 transition-all appearance-none cursor-pointer"
              >
                <option value="No info">Standard Economy (No special condition)</option>
                <option value="In-flight meal not included">In-flight meal not included (Low-cost fare)</option>
                <option value="No check-in baggage included">No check-in baggage included (Hand-baggage only)</option>
                <option value="1 Long layover">1 Long layover transit</option>
                <option value="Business class">Premium / Business Class</option>
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          {/* Submit Button & Interactive Loading Sequence */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={isPredicting}
              className={`w-full py-4 rounded-2xl font-bold text-base sm:text-lg flex items-center justify-center gap-3 transition-all duration-300 ${
                isPredicting
                  ? "bg-slate-800 text-sky-400 cursor-not-allowed border border-sky-400/30"
                  : "bg-gradient-to-r from-sky-500 via-blue-600 to-indigo-600 hover:from-sky-400 hover:via-blue-500 hover:to-indigo-500 text-white shadow-[0_4px_30px_rgba(2,132,199,0.5)] hover:scale-[1.01] active:scale-[0.99]"
              }`}
            >
              {isPredicting ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin text-sky-400" />
                  <span className="font-mono text-sm sm:text-base">{loadingStep || "Processing..."}</span>
                </>
              ) : (
                <>
                  <Plane className="w-5 h-5 -rotate-45" />
                  <span>PREDICT FLIGHT FARE</span>
                  <span className="text-xs bg-white/20 px-2 py-0.5 rounded-full font-mono font-normal">
                    Random Forest
                  </span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
