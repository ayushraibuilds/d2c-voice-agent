'use client';

import { useState } from 'react';
import { Play, Pause, Activity, Globe, Database, PhoneCall, CheckCircle } from 'lucide-react';
import Link from 'next/link';

export default function LandingPage() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const toggleAudio = () => {
    // Mock audio play action
    setIsPlaying(!isPlaying);
  };

  const handleWaitlist = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setStatus('loading');
    // Simulate Supabase insert
    setTimeout(() => {
      setStatus('success');
      setEmail('');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 overflow-hidden">
      {/* Header */}
      <header className="absolute top-0 inset-x-0 z-50 px-4 py-6 sm:px-6 lg:px-8 max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
            <PhoneCall className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold tracking-tight text-indigo-950">VocalD2C</span>
        </div>
        <nav className="flex items-center gap-6">
          <Link href="/admin" className="text-sm font-semibold text-indigo-600 hover:text-indigo-800 transition">
            Admin Dashboard
          </Link>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        {/* Background elements */}
        <div className="absolute top-0 right-0 -translate-y-12 translate-x-1/3">
          <div className="w-[600px] h-[600px] bg-indigo-200/40 rounded-full blur-3xl opacity-50"></div>
        </div>
        <div className="absolute bottom-0 left-0 translate-y-1/3 -translate-x-1/3">
          <div className="w-[500px] h-[500px] bg-fuchsia-200/40 rounded-full blur-3xl opacity-50"></div>
        </div>

        <div className="relative text-center max-w-3xl mx-auto">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-indigo-950 mb-8 leading-tight">
            Customer support via <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-fuchsia-600">WhatsApp Voice Notes.</span>
          </h1>
          <p className="text-xl text-slate-600 mb-10 leading-relaxed max-w-2xl mx-auto font-medium">
            Your customers hate typing. Let them speak natively in Hindi, English or Hinglish. 
            Our AI voice agent plugs directly into Shopify to track orders, process refunds, and answer FAQs.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <div className={`p-1.5 rounded-full bg-slate-100 flex items-center pr-4 shadow-sm border border-slate-200 transition-all ${isPlaying ? 'ring-2 ring-indigo-500 bg-indigo-50 border-indigo-200' : ''}`}>
              <button 
                onClick={toggleAudio}
                className="w-12 h-12 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full flex items-center justify-center shadow-md transition-transform active:scale-95"
              >
                {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-1" />}
              </button>
              <div className="ml-4 mr-6">
                <div className="text-sm font-semibold text-slate-900">Listen to an AI Call</div>
                <div className="text-xs text-slate-500 flex items-center gap-1">
                  <Activity className="w-3 h-3 text-indigo-500" />
                  &quot;Mera order kab aayega?&quot;
                </div>
              </div>
            </div>

            <form onSubmit={handleWaitlist} className="relative flex items-center w-full sm:w-auto mt-4 sm:mt-0">
              <input
                type="email"
                required
                disabled={status === 'success' || status === 'loading'}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                className="w-full sm:w-72 bg-white px-6 py-4 rounded-full border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent pr-32 shadow-sm"
              />
              <button
                type="submit"
                disabled={status === 'success' || status === 'loading'}
                className="absolute right-1.5 top-1.5 bottom-1.5 bg-indigo-950 hover:bg-slate-900 text-white px-5 rounded-full text-sm font-bold transition flex items-center justify-center disabled:opacity-80 disabled:cursor-not-allowed min-w-[100px]"
              >
                {status === 'loading' ? 'Joining...' : status === 'success' ? <CheckCircle className="w-4 h-4 ml-1 text-green-400" /> : 'Join Waitlist'}
              </button>
            </form>
          </div>
          
          {status === 'success' && (
            <p className="mt-4 text-sm font-medium text-green-600 animate-fade-in">
              You&apos;re on the list! We&apos;ll reach out soon.
            </p>
          )}

          {/* Integration Logos */}
          <div className="mt-20 pt-10 border-t border-slate-200/60">
            <p className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Seamlessly integrates with</p>
            <div className="flex flex-wrap items-center justify-center gap-8 md:gap-16 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
              <div className="flex items-center gap-2 font-bold text-xl"><Globe /> Shopify</div>
              <div className="flex items-center gap-2 font-bold text-xl"><Database /> WooCommerce</div>
              <div className="flex items-center gap-2 font-bold text-xl"><MessageSquareIcon /> WhatsApp</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

function MessageSquareIcon() {
  return (
    <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
    </svg>
  );
}
