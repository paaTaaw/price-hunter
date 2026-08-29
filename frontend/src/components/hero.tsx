"use client";

import { ArrowRight, Search, Sparkles } from "lucide-react";
import { motion } from "motion/react";
import { useRouter } from "next/navigation";
import { useState } from "react";

export function Hero() {
  const router = useRouter();
  const [query, setQuery] = useState("");

  function handleSearch(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery) return;

    router.push(`/search?q=${encodeURIComponent(trimmedQuery)}`);
  }

  return (
    <section className="relative overflow-hidden border-b border-white/5">
      {/* Background glow */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-[-180px] h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-lime-400/[0.06] blur-[120px]" />

        <div className="absolute bottom-[-200px] left-[-100px] h-[400px] w-[400px] rounded-full bg-blue-500/[0.04] blur-[120px]" />
      </div>

      {/* Grid background */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.025]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,1) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      <div className="relative mx-auto max-w-7xl px-6 pb-24 pt-20 md:pb-32 md:pt-28">
        {/* Announcement */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8 flex justify-center"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-lime-400/20 bg-lime-400/[0.06] px-4 py-2 text-xs text-lime-300">
            <Sparkles size={14} />

            <span>
              AI-powered price hunting is here
            </span>
          </div>
        </motion.div>

        {/* Main heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mx-auto max-w-5xl text-center"
        >
          <h1 className="text-5xl font-semibold leading-[0.95] tracking-[-0.055em] text-white sm:text-6xl md:text-7xl lg:text-8xl">
            Find it.
            <br />

            <span className="text-lime-400">
              Pay less.
            </span>
          </h1>

          <p className="mx-auto mt-7 max-w-2xl text-base leading-7 text-zinc-500 sm:text-lg">
            Search any product and let Price Hunter scan
            the web to find the best deal available.
          </p>
        </motion.div>

        {/* Search */}
        <motion.form
          onSubmit={handleSearch}
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mx-auto mt-10 max-w-3xl"
        >
          <div className="group flex items-center rounded-2xl border border-white/10 bg-white/[0.045] p-2 shadow-2xl shadow-black/20 backdrop-blur-xl transition duration-300 focus-within:border-lime-400/30 focus-within:bg-white/[0.06]">
            <Search
              size={21}
              className="ml-4 shrink-0 text-zinc-600 transition group-focus-within:text-lime-400"
            />

            <input
              type="text"
              value={query}
              onChange={(event) =>
                setQuery(event.target.value)
              }
              placeholder="What are you looking for?"
              className="h-14 min-w-0 flex-1 bg-transparent px-4 text-base text-white outline-none placeholder:text-zinc-600"
            />

            <button
              type="submit"
              className="flex h-14 items-center gap-2 rounded-xl bg-lime-400 px-5 text-sm font-semibold text-black transition hover:bg-lime-300 active:scale-[0.98]"
            >
              <span className="hidden sm:inline">
                Find the lowest price
              </span>

              <span className="sm:hidden">
                Search
              </span>

              <ArrowRight size={17} />
            </button>
          </div>
        </motion.form>

        {/* Example searches */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.35 }}
          className="mt-5 flex flex-wrap items-center justify-center gap-2 text-xs"
        >
          <span className="text-zinc-700">
            Try:
          </span>

          {[
            "iPhone 17 Pro",
            "MacBook Air",
            "Sony headphones",
            "Gaming laptop",
          ].map((item) => (
            <button
              key={item}
              type="button"
              onClick={() => {
                setQuery(item);
              }}
              className="rounded-full border border-white/5 px-3 py-1.5 text-zinc-600 transition hover:border-white/10 hover:text-zinc-300"
            >
              {item}
            </button>
          ))}
        </motion.div>

        {/* Trust / value indicators */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.45 }}
          className="mx-auto mt-16 grid max-w-2xl grid-cols-3 border-y border-white/5 py-6"
        >
          <div className="text-center">
            <div className="text-lg font-semibold text-white">
              100%
            </div>

            <div className="mt-1 text-[11px] uppercase tracking-wider text-zinc-700">
              Price focused
            </div>
          </div>

          <div className="border-x border-white/5 text-center">
            <div className="text-lg font-semibold text-white">
              Real-time
            </div>

            <div className="mt-1 text-[11px] uppercase tracking-wider text-zinc-700">
              Price checks
            </div>
          </div>

          <div className="text-center">
            <div className="text-lg font-semibold text-white">
              AI
            </div>

            <div className="mt-1 text-[11px] uppercase tracking-wider text-zinc-700">
              Smart matching
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}