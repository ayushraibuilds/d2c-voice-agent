"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export function Hero() {
    return (
        <section className="relative overflow-hidden bg-slate-950 pt-24 pb-32 sm:pt-32 sm:pb-40">
            {/* Background Glow */}
            <div className="absolute top-1/2 left-1/2 -z-10 -translate-x-1/2 -translate-y-1/2">
                <div className="h-[400px] w-[800px] rounded-full bg-indigo-600/20 blur-[100px]" />
            </div>

            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-3xl text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5 }}
                        className="mb-8 flex justify-center"
                    >
                        <span className="inline-flex items-center rounded-full bg-indigo-500/10 px-3 py-1 text-sm font-medium text-indigo-400 ring-1 ring-inset ring-indigo-500/20">
                            <span className="mr-2 flex h-2 w-2 rounded-full bg-indigo-500" />
                            Now integrating with ONDC & Shopify
                        </span>
                    </motion.div>

                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-4xl font-bold tracking-tight text-white sm:text-6xl"
                    >
                        Tier-2/3 Customer Support <br className="hidden sm:block" />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">
                            Solved with Voice AI
                        </span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="mt-6 text-lg leading-8 text-gray-300"
                    >
                        Empower your Indian D2C brand with a WhatsApp support agent that understands multilingual voice notes, tracks orders instantly, and hands off to human agents when needed.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="mt-10 flex items-center justify-center gap-x-6"
                    >
                        <a
                            href="#"
                            className="rounded-md bg-indigo-500 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-400 transition-colors flex items-center gap-2"
                        >
                            Book a Demo <ArrowRight className="h-4 w-4" />
                        </a>
                        <a href="#features" className="text-sm font-semibold leading-6 text-white hover:text-gray-300 transition-colors">
                            Explore Features <span aria-hidden="true">→</span>
                        </a>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
