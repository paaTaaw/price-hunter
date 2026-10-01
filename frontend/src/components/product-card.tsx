"use client";

import { ExternalLink, Star } from "lucide-react";

export interface ProductCardData {
  id?: string;
  name?: string;
  title?: string;

  brand?: string;
  category?: string;

  price?: number;
  best_price?: number;

  old_price?: number;
  oldPrice?: number;

  currency?: string;

  store?: string;
  seller?: string;

  rating?: number;
  reviews?: number;

  image?: string;
  url?: string;

  discount?: number;

  in_stock?: boolean;
  inStock?: boolean;

  shipping?: number;

  offer_count?: number;

  updatedAt?: string;
  checked_at?: string;
}

interface ProductCardProps {
  product: ProductCardData;
}

export default function ProductCard({
  product,
}: ProductCardProps) {
  const productTitle =
    product.title ||
    product.name ||
    "Unnamed product";

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

  const currency = product.currency || "NPR";

  const discount =
    typeof product.discount === "number"
      ? product.discount
      : oldPrice > price
        ? Math.round(
            ((oldPrice - price) / oldPrice) * 100
          )
        : 0;

  const inStock =
    typeof product.in_stock === "boolean"
      ? product.in_stock
      : typeof product.inStock === "boolean"
        ? product.inStock
        : true;

  const rating =
    typeof product.rating === "number"
      ? product.rating
      : 0;

  const reviews =
    typeof product.reviews === "number"
      ? product.reviews
      : 0;

  const shipping =
    typeof product.shipping === "number"
      ? product.shipping
      : 0;

  const totalPrice = price + shipping;

  return (
    <article className="group overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] shadow-sm transition-all duration-200 hover:-translate-y-1 hover:bg-white/[0.05] hover:shadow-xl">
      {/* Product Image */}
      <div className="relative aspect-square overflow-hidden bg-zinc-950">
        {product.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={product.image}
            alt={productTitle}
            className="h-full w-full object-contain p-4 transition-transform duration-300 group-hover:scale-105"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-zinc-600">
            No image available
          </div>
        )}

        {/* Discount */}
        {discount > 0 && (
          <span className="absolute left-3 top-3 rounded-full bg-red-500 px-3 py-1 text-xs font-bold text-white shadow-lg">
            -{discount}%
          </span>
        )}

        {/* Stock */}
        {!inStock && (
          <span className="absolute right-3 top-3 rounded-full bg-black/80 px-3 py-1 text-xs font-medium text-white">
            Out of stock
          </span>
        )}
      </div>

      {/* Product Information */}
      <div className="space-y-3 p-4">
        {/* Store */}
        <div className="flex items-center justify-between gap-3">
          <p className="text-xs font-medium uppercase tracking-wider text-zinc-500">
            {product.store || "Unknown store"}
          </p>

          {product.seller && (
            <p className="truncate text-xs text-zinc-600">
              {product.seller}
            </p>
          )}
        </div>

        {/* Brand */}
        {product.brand && (
          <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
            {product.brand}
          </p>
        )}

        {/* Name */}
        <h3 className="line-clamp-2 min-h-[3rem] text-sm font-semibold leading-6 text-white">
          {productTitle}
        </h3>

        {/* Rating */}
        {(rating > 0 || reviews > 0) && (
          <div className="flex items-center gap-2">
            <Star className="h-4 w-4 fill-current text-yellow-400" />

            <span className="text-sm font-medium text-white">
              {rating.toFixed(1)}
            </span>

            {reviews > 0 && (
              <span className="text-xs text-zinc-500">
                ({reviews.toLocaleString()})
              </span>
            )}
          </div>
        )}

        {/* Price */}
        <div>
          <div className="flex flex-wrap items-baseline gap-2">
            <span className="text-xl font-bold text-white">
              {currency} {price.toLocaleString()}
            </span>

            {oldPrice > price && (
              <span className="text-sm text-zinc-600 line-through">
                {currency} {oldPrice.toLocaleString()}
              </span>
            )}
          </div>

          {/* Shipping */}
          {shipping > 0 && (
            <p className="mt-1 text-xs text-zinc-500">
              + {currency} {shipping.toLocaleString()} shipping
            </p>
          )}

          {/* Total */}
          {shipping > 0 && (
            <p className="mt-1 text-xs font-medium text-zinc-400">
              Total: {currency} {totalPrice.toLocaleString()}
            </p>
          )}
        </div>

        {/* Offers */}
        {typeof product.offer_count === "number" &&
          product.offer_count > 1 && (
            <p className="text-xs text-zinc-500">
              {product.offer_count} offers available
            </p>
          )}

        {/* View Deal */}
        {product.url ? (
          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex w-full items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-sm font-semibold text-black transition hover:bg-zinc-200"
          >
            View Deal
            <ExternalLink className="h-4 w-4" />
          </a>
        ) : (
          <button
            type="button"
            disabled
            className="flex w-full cursor-not-allowed items-center justify-center rounded-lg bg-zinc-800 px-4 py-2.5 text-sm font-medium text-zinc-500"
          >
            Deal unavailable
          </button>
        )}
      </div>
    </article>
  );
}