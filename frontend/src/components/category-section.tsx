"use client";

import { ArrowRight } from "lucide-react";
import { motion } from "motion/react";

const categories = [
  {
    name: "Phones",
    description: "Find the best smartphone prices.",
    symbol: "01",
  },
  {
    name: "Laptops",
    description: "Compare laptops before you buy.",
    symbol: "02",
  },
  {
    name: "Headphones",
    description: "Discover audio deals.",
    symbol: "03",
  },
  {
    name: "Gaming",
    description: "Hunt gaming hardware & gear.",
    symbol: "04",
  },
];

export function CategorySection() {
  return (
    <section
      id="categories"
      className="mx-auto max-w-7xl px-6 py-24"
    >
      <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-medium text-lime-400">
            DISCOVER
          </p>

          <h2 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">
            What are you hunting for?
          </h2>
        </div>

        <button className="flex items-center gap-2 text-sm text-zinc-400 transition hover:text-white">
          Explore everything
          <ArrowRight size={16} />
        </button>
      </div>

      <div className="mt-10 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {categories.map((category) => (
          <motion.button
            key={category.name}
            whileHover={{ y: -5 }}
            transition={{ duration: 0.25 }}
            className="group rounded-2xl border border-white/5 bg-white/[0.025] p-7 text-left transition hover:border-white/10 hover:bg-white/[0.05]"
          >
            <div className="flex items-start justify-between">
              <span className="text-xs text-zinc-700">
                {category.symbol}
              </span>

              <ArrowRight
                size={16}
                className="text-zinc-700 transition group-hover:translate-x-1 group-hover:text-lime-400"
              />
            </div>

            <div className="mt-10 text-lg font-medium">
              {category.name}
            </div>

            <div className="mt-2 text-sm leading-6 text-zinc-600 transition group-hover:text-zinc-400">
              {category.description}
            </div>
          </motion.button>
        ))}
      </div>
    </section>
  );
}