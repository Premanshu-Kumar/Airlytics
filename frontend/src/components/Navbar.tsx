"use client";

import React, { useState, useEffect } from "react";
import { Plane, BarChart3, Brain, Compass, Info, Menu, X, ShieldCheck } from "lucide-react";

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Search & Predict", href: "#predict", icon: Plane },
    { name: "Why This Price?", href: "#why-this-price", icon: Brain },
    { name: "Market Analytics", href: "#analytics", icon: BarChart3 },
    { name: "AI Architecture", href: "#models", icon: ShieldCheck },
    { name: "Methodology", href: "#about", icon: Info },
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[#070b14]/90 backdrop-blur-md border-b border-white/10 shadow-lg shadow-black/40 py-3"
          : "bg-transparent py-5"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Brand Logo */}
          <a href="#" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-sky-500/20 group-hover:scale-105 transition-transform">
              <Plane className="w-5 h-5 text-white transform -rotate-45" />
            </div>
            <div>
              <div className="text-xl font-bold tracking-wider text-white flex items-center gap-2">
                AIRLYTICS
                <span className="text-[10px] uppercase font-semibold px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/30">
                  AI Fare Engine
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">Smarter Flights. Smarter Prices.</p>
            </div>
          </a>

          {/* Desktop Nav Items */}
          <div className="hidden md:flex items-center gap-1 bg-slate-900/60 border border-white/5 rounded-full px-4 py-1.5 backdrop-blur-sm">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <a
                  key={link.name}
                  href={link.href}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white hover:bg-white/5 rounded-full transition-colors"
                >
                  <Icon className="w-3.5 h-3.5 text-sky-400" />
                  {link.name}
                </a>
              );
            })}
          </div>

          {/* Action CTA */}
          <div className="hidden md:flex items-center gap-3">
            <a
              href="#predict"
              className="px-4 py-2 rounded-full text-xs font-semibold bg-gradient-to-r from-sky-500 to-blue-600 text-white shadow-md shadow-sky-500/25 hover:shadow-sky-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-1.5"
            >
              <Plane className="w-3.5 h-3.5" />
              Predict Fare
            </a>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg bg-slate-800/60 border border-white/10 text-slate-300 hover:text-white"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown */}
        {mobileMenuOpen && (
          <div className="md:hidden mt-3 p-4 rounded-2xl bg-slate-900/95 border border-white/10 backdrop-blur-xl shadow-2xl flex flex-col gap-2">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <a
                  key={link.name}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-200 hover:bg-sky-500/10 hover:text-sky-400 transition-colors"
                >
                  <Icon className="w-4 h-4 text-sky-400" />
                  {link.name}
                </a>
              );
            })}
            <a
              href="#predict"
              onClick={() => setMobileMenuOpen(false)}
              className="mt-2 w-full py-2.5 rounded-xl text-center text-sm font-semibold bg-sky-500 text-white shadow-lg shadow-sky-500/25"
            >
              Predict Fare Now
            </a>
          </div>
        )}
      </div>
    </nav>
  );
}
