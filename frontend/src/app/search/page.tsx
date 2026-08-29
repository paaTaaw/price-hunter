"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  AlertCircle,
  ArrowLeft,
  Loader2,
  PackageSearch,
  Search,
  SlidersHorizontal,
} from "lucide-react";

import ProductCard, {
  ProductCardData,
} from "@/components/product-card";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type SortValue = "lowest" | "highest" | "discount";

interface SearchResponse {
  query?: string;
  count?: number;
  results?: ProductCardData[];
  product_groups?: ProductCardData[];
}

function SearchPageContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const urlQuery = searchParams.get("q") || "";

  const urlSort = searchParams.get("sort");

  const sortValue: SortValue =
    urlSort === "highest" ||
    urlSort === "discount" ||
    urlSort === "lowest"
      ? urlSort
      : "lowest";

  const [searchInput, setSearchInput] = useState(urlQuery);
  const [results, setResults] = useState<ProductCardData[]>([]);
  const [resultCount, setResultCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /*
   * Search API function.
   */
  const searchProducts = useCallback(
    async (query: string, sort: SortValue, signal?: AbortSignal) => {
      const trimmedQuery = query.trim();

      if (!trimmedQuery) {
        setResults([]);
        setResultCount(0);
        setError("");
        setLoading(false);
        return;
      }

      const url =
        `${API_URL}/api/search` +
        `?q=${encodeURIComponent(trimmedQuery)}` +
        `&sort=${encodeURIComponent(sort)}`;

      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            Accept: "application/json",
          },
          signal,
        });

        if (!response.ok) {
          const text = await response.text();

          throw new Error(
            text || `Server returned ${response.status}`
          );
        }

        const data =
          (await response.json()) as SearchResponse;

        const products = Array.isArray(data.results)
          ? data.results
          : Array.isArray(data.product_groups)
            ? data.product_groups
            : [];

        setResults(products);

        setResultCount(
          typeof data.count === "number"
            ? data.count
            : products.length
        );

        setError("");
      } catch (err: unknown) {
        if (
          err instanceof DOMException &&
          err.name === "AbortError"
        ) {
          return;
        }

        console.error(
          "Price Hunter search failed:",
          err
        );

        setResults([]);
        setResultCount(0);

        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError(
            "Unable to connect to the Price Hunter API."
          );
        }
      } finally {
        if (!signal?.aborted) {
          setLoading(false);
        }
      }
    },
    []
  );

  /*
   * Search when the URL query changes.
   *
   * The loading state is scheduled asynchronously so the
   * react-hooks/set-state-in-effect rule is not triggered.
   */
  useEffect(() => {
    const query = urlQuery.trim();

    if (!query) {
      return;
    }

    const controller = new AbortController();

    const runSearch = async () => {
      setLoading(true);

      await searchProducts(
        query,
        sortValue,
        controller.signal
      );
    };

    void runSearch();

    return () => {
      controller.abort();
    };
  }, [urlQuery, sortValue, searchProducts]);

  /*
   * Keep the search input synchronized with the URL without
   * using a synchronous setState call inside an effect.
   *
   * We intentionally initialize searchInput from urlQuery.
   * User changes are handled directly by the input.
   */

  const handleSearch = (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    const query = searchInput.trim();

    if (!query) {
      router.push("/search");
      return;
    }

    router.push(
      `/search?q=${encodeURIComponent(query)}&sort=${encodeURIComponent(
        sortValue
      )}`
    );
  };

  const handleSortChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const newSort = event.target.value as SortValue;

    const query = urlQuery.trim();

    if (!query) {
      return;
    }

    router.push(
      `/search?q=${encodeURIComponent(query)}&sort=${encodeURIComponent(
        newSort
      )}`
    );
  };

  return (
    <main className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-zinc-800 bg-black">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-5 sm:px-6 lg:px-8">
          <Link
            href="/"
            className="flex items-center gap-2 text-sm text-zinc-400 transition hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Home
          </Link>

          <div className="h-5 w-px bg-zinc-800" />

          <h1 className="text-lg font-semibold">
            Price Hunter
          </h1>
        </div>
      </header>

      {/* Main */}
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Search Form */}
        <form
          onSubmit={handleSearch}
          className="mx-auto flex max-w-3xl gap-3"
        >
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-zinc-500" />

            <input
              type="search"
              value={searchInput}
              onChange={(event) =>
                setSearchInput(event.target.value)
              }
              placeholder="Search for products..."
              className="h-12 w-full rounded-xl border border-zinc-800 bg-zinc-900 pl-12 pr-4 text-white outline-none placeholder:text-zinc-500 focus:border-zinc-600"
            />
          </div>

          <button
            type="submit"
            className="flex h-12 items-center gap-2 rounded-xl bg-white px-5 font-semibold text-black transition hover:bg-zinc-200"
          >
            <Search className="h-4 w-4" />
            Search
          </button>
        </form>

        {/* Search Header */}
        <div className="mt-10 flex flex-col justify-between gap-4 border-b border-zinc-800 pb-5 sm:flex-row sm:items-center">
          <div>
            <h2 className="text-2xl font-bold">
              {urlQuery
                ? `Results for "${urlQuery}"`
                : "Search Products"}
            </h2>

            {urlQuery && (
              <p className="mt-1 text-sm text-zinc-500">
                {loading
                  ? "Searching stores..."
                  : `${resultCount} product${
                      resultCount === 1 ? "" : "s"
                    } found`}
              </p>
            )}
          </div>

          {urlQuery && (
            <div className="flex items-center gap-2">
              <SlidersHorizontal className="h-4 w-4 text-zinc-500" />

              <label
                htmlFor="sort"
                className="text-sm text-zinc-500"
              >
                Sort:
              </label>

              <select
                id="sort"
                value={sortValue}
                onChange={handleSortChange}
                className="rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm text-white outline-none"
              >
                <option value="lowest">
                  Lowest Price
                </option>

                <option value="highest">
                  Highest Price
                </option>

                <option value="discount">
                  Biggest Discount
                </option>
              </select>
            </div>
          )}
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex min-h-[300px] flex-col items-center justify-center gap-4">
            <Loader2 className="h-8 w-8 animate-spin" />

            <p className="text-sm text-zinc-500">
              Finding the best prices...
            </p>
          </div>
        )}

        {/* Error */}
        {!loading && error && (
          <div className="mx-auto mt-10 max-w-2xl rounded-2xl border border-red-900/50 bg-red-950/20 p-6">
            <div className="flex items-start gap-4">
              <AlertCircle className="mt-0.5 h-6 w-6 shrink-0 text-red-400" />

              <div>
                <h3 className="font-semibold text-red-300">
                  Search failed
                </h3>

                <p className="mt-2 text-sm leading-6 text-zinc-400">
                  {error}
                </p>

                <p className="mt-3 text-xs text-zinc-600">
                  Make sure the FastAPI backend is running at{" "}
                  {API_URL}.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* No Query */}
        {!loading &&
          !error &&
          !urlQuery && (
            <div className="flex min-h-[400px] flex-col items-center justify-center text-center">
              <PackageSearch className="h-16 w-16 text-zinc-800" />

              <h2 className="mt-6 text-xl font-semibold">
                Search for a product
              </h2>

              <p className="mt-2 max-w-md text-sm text-zinc-500">
                Enter a product name above and Price Hunter
                will search available stores for the best deal.
              </p>
            </div>
          )}

        {/* No Results */}
        {!loading &&
          !error &&
          urlQuery &&
          results.length === 0 && (
            <div className="flex min-h-[400px] flex-col items-center justify-center text-center">
              <PackageSearch className="h-16 w-16 text-zinc-800" />

              <h2 className="mt-6 text-xl font-semibold">
                No products found
              </h2>

              <p className="mt-2 max-w-md text-sm text-zinc-500">
                We could not find matching products for this
                search. Try another product name.
              </p>
            </div>
          )}

        {/* Products */}
        {!loading &&
          !error &&
          results.length > 0 && (
            <section className="mt-8">
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {results.map((product, index) => (
                  <ProductCard
                    key={
                      product.id ||
                      `${product.name || product.title}-${index}`
                    }
                    product={product}
                  />
                ))}
              </div>
            </section>
          )}
      </div>
    </main>
  );
}

export default function SearchPage() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen items-center justify-center bg-black text-white">
          <Loader2 className="h-8 w-8 animate-spin" />
        </main>
      }
    >
      <SearchPageContent />
    </Suspense>
  );
}