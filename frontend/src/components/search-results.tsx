"use client";

import {
  ArrowUpDown,
  ExternalLink,
  Star,
} from "lucide-react";

import type { ProductCardData } from "./product-card";

interface SearchResultsProps {
  products: ProductCardData[];
  sort?: string;
  onSortChange?: (value: string) => void;
}

export default function SearchResults({
  products,
  sort = "lowest",
  onSortChange,
}: SearchResultsProps) {
  const sortedProducts = [...products].sort(
    (a, b) => {
      const aPrice =
        typeof a.price === "number"
          ? a.price
          : typeof a.best_price === "number"
            ? a.best_price
            : Number.MAX_SAFE_INTEGER;

      const bPrice =
        typeof b.price === "number"
          ? b.price
          : typeof b.best_price === "number"
            ? b.best_price
            : Number.MAX_SAFE_INTEGER;

      const aDiscount =
        typeof a.discount === "number"
          ? a.discount
          : 0;

      const bDiscount =
        typeof b.discount === "number"
          ? b.discount
          : 0;

      if (sort === "highest") {
        return bPrice - aPrice;
      }

      if (sort === "discount") {
        return bDiscount - aDiscount;
      }

      return aPrice - bPrice;
    }
  );

  if (sortedProducts.length === 0) {
    return null;
  }

  return (
    <section className="w-full">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-white">
            Products
          </h2>

          <p className="mt-1 text-sm text-zinc-500">
            {sortedProducts.length}{" "}
            {sortedProducts.length === 1
              ? "result"
              : "results"}
          </p>
        </div>

        {onSortChange && (
          <div className="flex items-center gap-2">
            <ArrowUpDown className="h-4 w-4 text-zinc-500" />

            <select
              value={sort}
              onChange={(event) =>
                onSortChange(event.target.value)
              }
              className="rounded-lg border border-white/10 bg-zinc-900 px-3 py-2 text-sm text-zinc-300 outline-none focus:border-white/20"
            >
              <option
                value="lowest"
                className="bg-zinc-950"
              >
                Lowest Price
              </option>

              <option
                value="highest"
                className="bg-zinc-950"
              >
                Highest Price
              </option>

              <option
                value="discount"
                className="bg-zinc-950"
              >
                Biggest Discount
              </option>
            </select>
          </div>
        )}
      </div>

      {/* Results */}
      <div className="space-y-3">
        {sortedProducts.map((product, index) => {
          const price =
            typeof product.price === "number"
              ? product.price
              : typeof product.best_price === "number"
                ? product.best_price
                : 0;

          const oldPrice =
            typeof product.old_price === "number"
              ? product.old_price
              : typeof product.oldPrice === "number"
                ? product.oldPrice
                : 0;

          const discount =
            typeof product.discount === "number"
              ? product.discount
              : 0;

          const rating =
            typeof product.rating === "number"
              ? product.rating
              : 0;

          const reviews =
            typeof product.reviews === "number"
              ? product.reviews
              : 0;

          const inStock =
            typeof product.in_stock === "boolean"
              ? product.in_stock
              : true;

          const key =
            product.id ||
            product.url ||
            `${product.name || "product"}-${index}`;

          return (
            <article
              key={key}
              className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4 transition hover:bg-white/[0.05] sm:flex-row sm:items-center"
            >
              {/* Image */}
              <div className="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-zinc-950">
                {product.image ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={product.image}
                    alt={product.name || "Product"}
                    className="h-full w-full object-contain"
                  />
                ) : (
                  <span className="text-xs text-zinc-600">
                    No image
                  </span>
                )}
              </div>

              {/* Product info */}
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <p className="text-xs uppercase tracking-wide text-zinc-600">
                    {product.store || "Unknown store"}
                  </p>

                  {!inStock && (
                    <span className="rounded-full bg-red-500/10 px-2 py-0.5 text-[10px] font-medium text-red-400">
                      Out of stock
                    </span>
                  )}
                </div>

                <h3 className="mt-1 line-clamp-2 text-base font-medium text-white">
                  {product.name || "Unnamed product"}
                </h3>

                {product.brand && (
                  <p className="mt-1 text-sm text-zinc-500">
                    {product.brand}
                  </p>
                )}

                <div className="mt-2 flex flex-wrap items-center gap-3">
                  {rating > 0 && (
                    <span className="flex items-center gap-1 text-xs text-zinc-400">
                      <Star className="h-3.5 w-3.5 fill-current text-yellow-400" />
                      {rating.toFixed(1)}
                    </span>
                  )}

                  {reviews > 0 && (
                    <span className="text-xs text-zinc-600">
                      {reviews.toLocaleString()} reviews
                    </span>
                  )}

                  {discount > 0 && (
                    <span className="rounded-md bg-green-500/10 px-2 py-1 text-xs font-medium text-green-400">
                      {discount}% OFF
                    </span>
                  )}
                </div>
              </div>

              {/* Price */}
              <div className="shrink-0 sm:text-right">
                <div className="text-xl font-semibold text-white">
                  {product.currency || "NPR"}{" "}
                  {price.toLocaleString()}
                </div>

                {oldPrice > price && (
                  <div className="mt-1 text-sm text-zinc-600 line-through">
                    {product.currency || "NPR"}{" "}
                    {oldPrice.toLocaleString()}
                  </div>
                )}

                {typeof product.shipping === "number" &&
                  product.shipping > 0 && (
                    <div className="mt-1 text-xs text-zinc-500">
                      + shipping{" "}
                      {product.shipping.toLocaleString()}
                    </div>
                  )}
              </div>

              {/* Link */}
              {product.url && (
                <a
                  href={product.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex shrink-0 items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-medium text-black transition hover:bg-zinc-200"
                >
                  View Deal
                  <ExternalLink className="h-4 w-4" />
                </a>
              )}
            </article>
          );
        })}
      </div>
    </section>
  );
}