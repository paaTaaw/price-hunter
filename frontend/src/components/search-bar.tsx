"use client";

import { ArrowLeft, Search, SlidersHorizontal } from "lucide-react";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

type SearchBarProps = {
  initialQuery?: string;
  onFilterToggle?: () => void;
};

export function SearchBar({
  initialQuery = "",
  onFilterToggle,
}: SearchBarProps) {
  const router = useRouter();
  const [query, setQuery] = useState(initialQuery);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedQuery = query.trim();

    if (!trimmedQuery) return;

    router.push(`/search?q=${encodeURIComponent(trimmedQuery)}`);
  }

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={() => router.push("/")}
        aria-label="Back to home"
        className="hidden h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-white/10 text-zinc-400 transition hover:border-white/20 hover:text-white md:flex"
      >
        <ArrowLeft size={18} />
      </button>

      <form onSubmit={handleSubmit} className="flex flex-1">
        <div className="group flex w-full items-center rounded-xl border border-white/10 bg-white/[0.04] p-1.5 transition focus-within:border-lime-400/40">
          <Search
            size={19}
            className="ml-3 shrink-0 text-zinc-500"
          />

          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search products..."
            className="h-10 min-w-0 flex-1 bg-transparent px-3 text-sm text-white outline-none placeholder:text-zinc-600"
          />

          <button
            type="submit"
            className="flex h-10 items-center gap-2 rounded-lg bg-lime-400 px-4 text-sm font-medium text-black transition hover:bg-lime-300"
          >
            Search
          </button>
        </div>
      </form>

      <button
        onClick={onFilterToggle}
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-white/10 text-zinc-400 transition hover:border-white/20 hover:text-white lg:hidden"
        aria-label="Open filters"
      >
        <SlidersHorizontal size={18} />
      </button>
    </div>
  );
}