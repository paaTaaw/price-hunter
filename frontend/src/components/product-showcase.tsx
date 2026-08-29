"use client";

import { useRouter } from "next/navigation";

import { products } from "@/data/products";
import ProductCard from "@/components/product-card";

export function ProductShowcase() {
  const router = useRouter();

  const handleViewAll = () => {
    router.push("/search?q=");
  };

  return (
    <section className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-8 flex items-end justify-between gap-4">
        <div>
          <p className="mb-2 text-sm font-semibold uppercase tracking-wider text-primary">
            Featured Deals
          </p>

          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Popular Products
          </h2>

          <p className="mt-2 max-w-2xl text-muted-foreground">
            Compare prices from different stores and find the best deal.
          </p>
        </div>

        <button
          type="button"
          onClick={handleViewAll}
          className="hidden rounded-lg border px-4 py-2 text-sm font-medium transition-colors hover:bg-muted sm:block"
        >
          View All
        </button>
      </div>

      {products.length === 0 ? (
        <div className="rounded-2xl border border-dashed p-12 text-center">
          <p className="text-muted-foreground">
            No products available.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {products.slice(0, 8).map((product) => (
            <ProductCard
              key={product.id}
              product={product}
            />
          ))}
        </div>
      )}

      <button
        type="button"
        onClick={handleViewAll}
        className="mt-8 w-full rounded-lg border px-4 py-3 text-sm font-medium transition-colors hover:bg-muted sm:hidden"
      >
        View All Products
      </button>
    </section>
  );
}