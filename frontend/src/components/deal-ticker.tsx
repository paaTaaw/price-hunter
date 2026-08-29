"use client";

import { TrendingDown } from "lucide-react";
import { motion } from "motion/react";

const deals = [
  "iPhone 17 Pro ↓ 8%",
  "MacBook Air M5 ↓ 13%",
  "Sony WH-1000XM6 ↓ 25%",
  "PlayStation 5 ↓ 12%",
  "RTX 5070 ↓ 18%",
  "AirPods Pro ↓ 16%",
];

export function DealTicker() {
  return (
    <section className="overflow-hidden border-y border-white/5 bg-white/[0.015]">
      <div className="mx-auto flex max-w-7xl items-center">
        <div className="z-10 flex shrink-0 items-center gap-2 border-r border-white/5 bg-[#09090b] px-6 py-4 text-xs font-medium text-lime-400">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-lime-400 opacity-75" />

            <span className="relative inline-flex h-2 w-2 rounded-full bg-lime-400" />
          </span>

          LIVE
        </div>

        <div className="relative flex overflow-hidden">
          <motion.div
            animate={{ x: ["0%", "-50%"] }}
            transition={{
              duration: 25,
              repeat: Infinity,
              ease: "linear",
            }}
            className="flex min-w-max"
          >
            {[...deals, ...deals].map((deal, index) => (
              <div
                key={`${deal}-${index}`}
                className="flex items-center gap-2 px-8 py-4 text-xs text-zinc-500"
              >
                <TrendingDown
                  size={13}
                  className="text-lime-400"
                />

                {deal}
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  );
}