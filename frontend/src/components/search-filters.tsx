"use client";

import { Check, RotateCcw } from "lucide-react";

interface SearchFiltersProps {
  saleOnly: boolean;
  setSaleOnly: (value: boolean) => void;

  selectedStore: string;
  setSelectedStore: (value: string) => void;

  maxPrice: number;
  setMaxPrice: (value: number) => void;

  timeRange: string;
  setTimeRange: (value: string) => void;

  onReset: () => void;
}

const stores = [
  "All stores",
  "Daraz Nepal",
  "Demo Store",
  "Demo Store 2",
];

export function SearchFilters({
  saleOnly,
  setSaleOnly,
  selectedStore,
  setSelectedStore,
  maxPrice,
  setMaxPrice,
  timeRange,
  setTimeRange,
  onReset,
}: SearchFiltersProps) {
  return (
    <aside className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="font-medium text-white">
          Filters
        </h2>

        <button
          type="button"
          onClick={onReset}
          className="flex items-center gap-1.5 text-xs text-zinc-600 transition hover:text-white"
        >
          <RotateCcw size={12} />
          Reset
        </button>
      </div>

      {/* Sale */}
      <div>
        <p className="mb-4 text-xs font-medium uppercase tracking-wider text-zinc-600">
          Deals
        </p>

        <button
          type="button"
          onClick={() => setSaleOnly(!saleOnly)}
          className="flex w-full items-center justify-between text-sm"
        >
          <span className="text-zinc-400">
            On sale only
          </span>

          <span
            className={`flex h-5 w-5 items-center justify-center rounded-md border transition ${
              saleOnly
                ? "border-lime-400 bg-lime-400 text-black"
                : "border-white/10"
            }`}
          >
            {saleOnly && <Check size={13} />}
          </span>
        </button>
      </div>

      {/* Store */}
      <div>
        <p className="mb-4 text-xs font-medium uppercase tracking-wider text-zinc-600">
          Store
        </p>

        <div className="space-y-3">
          {stores.map((store) => (
            <button
              type="button"
              key={store}
              onClick={() => setSelectedStore(store)}
              className="flex w-full items-center justify-between text-sm"
            >
              <span
                className={
                  selectedStore === store
                    ? "text-white"
                    : "text-zinc-500"
                }
              >
                {store}
              </span>

              <span
                className={`h-4 w-4 rounded-full border ${
                  selectedStore === store
                    ? "border-lime-400 bg-lime-400"
                    : "border-white/10"
                }`}
              />
            </button>
          ))}
        </div>
      </div>

      {/* Price */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
            Maximum price
          </p>

          <span className="text-xs text-zinc-400">
            Rs. {maxPrice.toLocaleString()}
          </span>
        </div>

        <input
          type="range"
          min="50000"
          max="200000"
          step="5000"
          value={maxPrice}
          onChange={(event) =>
            setMaxPrice(Number(event.target.value))
          }
          className="w-full accent-lime-400"
        />

        <div className="mt-2 flex justify-between text-[11px] text-zinc-700">
          <span>Rs. 50K</span>
          <span>Rs. 200K+</span>
        </div>
      </div>

      {/* Time */}
      <div>
        <p className="mb-4 text-xs font-medium uppercase tracking-wider text-zinc-600">
          Updated
        </p>

        <div className="space-y-2">
          {[
            ["any", "Any time"],
            ["hour", "Last hour"],
            ["day", "Today"],
            ["week", "This week"],
          ].map(([value, label]) => (
            <button
              type="button"
              key={value}
              onClick={() => setTimeRange(value)}
              className={`w-full rounded-lg px-3 py-2 text-left text-sm transition ${
                timeRange === value
                  ? "bg-white/5 text-white"
                  : "text-zinc-500 hover:bg-white/[0.03] hover:text-zinc-300"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}