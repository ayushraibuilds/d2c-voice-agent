import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { InteractiveChat } from "@/components/InteractiveChat";
import { HowItWorks } from "@/components/HowItWorks";
import { FeatureGrid } from "@/components/FeatureGrid";
import { Integrations } from "@/components/Integrations";
import { Pricing } from "@/components/Pricing";
import { Contact } from "@/components/Contact";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Navbar />
      <Hero />
      <InteractiveChat />
      <HowItWorks />
      <FeatureGrid />
      <Integrations />
      <Pricing />
      <Contact />

      {/* Footer */}
      <footer className="bg-slate-950 py-16 border-t border-white/10">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Brand */}
            <div className="md:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center">
                  <span className="text-white font-bold text-sm">V</span>
                </div>
                <span className="text-white font-semibold text-lg">VoiceAgent</span>
              </div>
              <p className="text-sm text-gray-400 max-w-sm leading-relaxed">
                Enterprise-grade voice-first WhatsApp AI support for Indian D2C
                brands. Built on ONDC, powered by Groq.
              </p>
            </div>

            {/* Product Links */}
            <div>
              <h4 className="text-sm font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2">
                <li><a href="#features" className="text-sm text-gray-400 hover:text-white transition-colors">Features</a></li>
                <li><a href="#how-it-works" className="text-sm text-gray-400 hover:text-white transition-colors">How it Works</a></li>
                <li><a href="#pricing" className="text-sm text-gray-400 hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#integrations" className="text-sm text-gray-400 hover:text-white transition-colors">Integrations</a></li>
              </ul>
            </div>

            {/* Company Links */}
            <div>
              <h4 className="text-sm font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2">
                <li><a href="#contact" className="text-sm text-gray-400 hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-sm text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>

          <div className="mt-12 pt-8 border-t border-white/10 text-center">
            <p className="text-sm text-gray-500">
              © 2026 VoiceAgent. Built for Indian E-commerce.
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
