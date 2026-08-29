"use client";

import Image from "next/image";
import { ExternalLink, Star } from "lucide-react";

/*
 * Product data structure
 *
 * Both "name" and "title" are supported because different
 * parts of the application may use either property.
 */
export interface ProductCardData {
  id: string;

  name: string;

  /*
   * Some API/search components use "title".
   * It is optional because our local product data primarily uses "name".
   */
  title?: string;

  brand: string;
  category: string;

  price: number;
  oldPrice?: number;

  currency: string;
  store: string;

  rating: number;
  reviews: number;

  image: string;
  url: string;

  discount?: number;

  inStock: boolean;
  updatedAt: string;
}

/*
 * Props received by ProductCard.
 */
export interface ProductCardProps {
  product: ProductCardData;
}

/*
 * Product Card Component
 */
export default function ProductCard({
  product,
}: ProductCardProps) {
  const {
    name,
    title,
    brand,
    price,
    oldPrice,
    currency,
    store,
    rating,
    reviews,
    image,
    url,
    discount,
    inStock,
  } = product;

  /*
   * Use title when available.
   * Otherwise fall back to name.
   */
  const productTitle = title || name;

  /*
   * Calculate discount when it is not supplied.
   */
  const calculatedDiscount =
    typeof discount === "number"
      ? discount
      : typeof oldPrice === "number" && oldPrice > price
        ? Math.round(((oldPrice - price) / oldPrice) * 100)
        : 0;

  return (
    <article className="group overflow-hidden rounded-2xl border bg-card shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-lg">
      {/* Product Image */}
      <div className="relative aspect-square overflow-hidden bg-muted">
        {image ? (
          <Image
            src={image}
            alt={productTitle}
            fill
            className="object-cover transition-transform duration-300 group-hover:scale-105"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
            No image available
          </div>
        )}

        {/* Discount Badge */}
        {calculatedDiscount > 0 && (
          <span className="absolute left-3 top-3 rounded-full bg-red-500 px-3 py-1 text-xs font-semibold text-white">
            -{calculatedDiscount}%
          </span>
        )}

        {/* Stock Badge */}
        {!inStock && (
          <span className="absolute right-3 top-3 rounded-full bg-black/75 px-3 py-1 text-xs font-medium text-white">
            Out of stock
          </span>
        )}
      </div>

      {/* Product Information */}
      <div className="space-y-3 p-4">
        {/* Brand + Product Name */}
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
            {brand}
          </p>

          <h3 className="mt-1 line-clamp-2 min-h-[3rem] text-sm font-semibold">
            {productTitle}
          </h3>
        </div>

        {/* Rating */}
        <div className="flex items-center gap-2">
          <Star className="h-4 w-4 fill-current" />

          <span className="text-sm font-medium">
            {Number(rating || 0).toFixed(1)}
          </span>

          <span className="text-xs text-muted-foreground">
            ({reviews || 0})
          </span>
        </div>

        {/* Price */}
        <div>
          <div className="flex items-baseline gap-2">
            <span className="text-xl font-bold">
              {currency} {Number(price || 0).toLocaleString()}
            </span>

            {typeof oldPrice === "number" && oldPrice > price && (
              <span className="text-sm text-muted-foreground line-through">
                {currency} {oldPrice.toLocaleString()}
              </span>
            )}
          </div>

          <p className="mt-1 text-xs text-muted-foreground">
            Available at {store}
          </p>
        </div>

        {/* View Deal */}
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground transition-opacity hover:opacity-90"
        >
          View Deal
          <ExternalLink className="h-4 w-4" />
        </a>
      </div>
    </article>
  );
}