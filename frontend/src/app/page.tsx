import { CategorySection } from "@/components/category-section";
import { DealTicker } from "@/components/deal-ticker";
import { Footer } from "@/components/footer";
import { Hero } from "@/components/hero";
import { Navbar } from "@/components/navbar";
import { ProductShowcase } from "@/components/product-showcase";
import { Stats } from "@/components/stats";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#09090b] text-white">
      <Navbar />

      <Hero />

      <DealTicker />

      <Stats />

      <ProductShowcase />

      <CategorySection />

      <Footer />
    </main>
  );
}