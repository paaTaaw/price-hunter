"use client";

import { motion } from "motion/react";
import { Globe2, Package, TrendingDown } from "lucide-react";

const stats = [
  {
    icon: Package,
    value: "10K+",
    label: "Products tracked",
  },
  {
    icon: TrendingDown,
    value: "Real-time",
    label: "Price monitoring",
  },
  {
    icon: Globe2,
    value: "Multi-store",
    label: "Comparison engine",
  },
];

export function Stats() {
  return (
    <section className="border-b border-white/5">
      <div className="mx-auto grid max-w-5xl grid-cols-1 divide-y divide-white/5 md:grid-cols-3 md:divide-x md:divide-y-0">
        {stats.map((stat, index) => {
          const Icon = stat.icon;

          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="px-8 py-10 text-center"
            >
              <div className="mb-3 flex justify-center">
                <Icon
                  size={20}
                  className="text-lime-400"
                />
              </div>

              <div className="text-3xl font-semibold tracking-tight">
                {stat.value}
              </div>

              <div className="mt-2 text-sm text-zinc-500">
                {stat.label}
              </div>
            </motion.div>
          );
        })}
      </div>
    </section>
  );
}