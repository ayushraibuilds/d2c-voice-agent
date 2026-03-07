import { Hero } from "@/components/Hero";
import { InteractiveChat } from "@/components/InteractiveChat";
import { FeatureGrid } from "@/components/FeatureGrid";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <InteractiveChat />
      <FeatureGrid />

      {/* Footer */}
      <footer className="bg-slate-950 py-12 text-center text-sm text-gray-400 border-t border-white/10">
        <p>© 2026 Voice-First D2C Agent. Built for Indian E-commerce.</p>
      </footer>
    </main>
  );
}
