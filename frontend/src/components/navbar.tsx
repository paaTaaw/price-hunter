"use client";

import { motion } from "motion/react";
import { Bell, Menu, Sparkles, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="relative z-50 mx-auto flex max-w-7xl items-center justify-between px-6 py-6"
    >
      {/* Logo */}
      <div className="flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-black">
          <Sparkles size={16} />
        </div>

        <div className="text-lg font-semibold tracking-[-0.03em]">
          PRICE<span className="text-lime-400">HUNTER</span>
        </div>
      </div>

      {/* Desktop navigation */}
      <div className="hidden items-center gap-8 text-sm text-zinc-400 md:flex">
        <a href="#" className="transition hover:text-white">
          Explore
        </a>

        <a href="#deals" className="transition hover:text-white">
          Deals
        </a>

        <a href="#categories" className="transition hover:text-white">
          Categories
        </a>

        <a href="#" className="transition hover:text-white">
          How it works
        </a>
      </div>

      {/* Desktop actions */}
      <div className="hidden items-center gap-3 md:flex">
        <button
          aria-label="Price alerts"
          className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 text-zinc-400 transition hover:border-white/20 hover:text-white"
        >
          <Bell size={16} />
        </button>

        <button className="rounded-full border border-white/10 px-5 py-2 text-sm transition hover:bg-white/5">
          Sign in
        </button>
      </div>

      {/* Mobile menu button */}
      <button
        onClick={() => setMobileOpen(!mobileOpen)}
        className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 md:hidden"
        aria-label="Toggle menu"
      >
        {mobileOpen ? <X size={18} /> : <Menu size={18} />}
      </button>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="absolute left-6 right-6 top-20 rounded-2xl border border-white/10 bg-zinc-950/95 p-5 shadow-2xl backdrop-blur-xl md:hidden">
          <div className="flex flex-col gap-5 text-sm text-zinc-400">
            <a href="#">Explore</a>
            <a href="#deals">Deals</a>
            <a href="#categories">Categories</a>
            <a href="#">How it works</a>

            <button className="rounded-xl border border-white/10 px-4 py-3 text-left text-white">
              Sign in
            </button>
          </div>
        </div>
      )}
    </motion.nav>
  );
}