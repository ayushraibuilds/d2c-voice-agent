"use client";

import { motion } from "framer-motion";
import { Mic, Brain, MessageSquare, Headphones } from "lucide-react";

const steps = [
    {
        icon: Mic,
        number: "01",
        title: "Customer Sends Voice Note",
        description:
            "Your customer sends a Hinglish voice note on WhatsApp — \"Bhaiya mera order kab aayega?\"",
        color: "from-green-500 to-emerald-600",
    },
    {
        icon: Brain,
        number: "02",
        title: "AI Transcribes & Understands",
        description:
            "Groq's Whisper transcribes in <500ms. LangGraph detects language, classifies intent, and extracts entities.",
        color: "from-indigo-500 to-purple-600",
    },
    {
        icon: MessageSquare,
        number: "03",
        title: "Instant Action & Reply",
        description:
            "The agent queries your order DB, processes refunds, or answers FAQs — then replies in the customer's language.",
        color: "from-cyan-500 to-blue-600",
    },
    {
        icon: Headphones,
        number: "04",
        title: "Smart Human Handoff",
        description:
            "If the AI detects frustration or can't resolve, it creates a ticket and seamlessly transfers to your support team.",
        color: "from-orange-500 to-red-500",
    },
];

export function HowItWorks() {
    return (
        <section id="how-it-works" className="bg-slate-950 py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-base font-semibold text-indigo-400">How it Works</h2>
                    <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        From voice note to resolution in seconds
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {steps.map((step, index) => (
                        <motion.div
                            key={step.number}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.15 }}
                            className="relative group"
                        >
                            {/* Connector line */}
                            {index < steps.length - 1 && (
                                <div className="hidden lg:block absolute top-10 left-[calc(50%+40px)] w-[calc(100%-40px)] h-[2px] bg-gradient-to-r from-white/20 to-transparent" />
                            )}

                            <div className="bg-white/5 rounded-2xl p-6 border border-white/10 hover:border-indigo-500/30 transition-all duration-300 hover:bg-white/[.07]">
                                <div
                                    className={`inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${step.color} mb-4 shadow-lg`}
                                >
                                    <step.icon className="h-6 w-6 text-white" />
                                </div>

                                <span className="text-xs font-bold text-indigo-400 tracking-widest">
                                    STEP {step.number}
                                </span>
                                <h3 className="mt-2 text-lg font-semibold text-white">
                                    {step.title}
                                </h3>
                                <p className="mt-2 text-sm text-gray-400 leading-relaxed">
                                    {step.description}
                                </p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
