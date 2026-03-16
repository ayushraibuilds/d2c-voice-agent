"use client";

import { motion } from "framer-motion";
import { Send, Mail, Phone, MapPin } from "lucide-react";
import { useState } from "react";

export function Contact() {
    const [submitted, setSubmitted] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitted(true);
        // In production, this would POST to an API
    };

    return (
        <section id="contact" className="bg-slate-900 py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
                    {/* Left — Info */}
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5 }}
                    >
                        <h2 className="text-base font-semibold text-indigo-400">Get Started</h2>
                        <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                            Book a personalized demo
                        </p>
                        <p className="mt-4 text-gray-400 leading-relaxed">
                            See how our voice-first AI agent can handle your customer support
                            in Hindi, Hinglish, and English — live on WhatsApp.
                        </p>

                        <div className="mt-10 space-y-6">
                            <div className="flex items-center gap-4">
                                <div className="h-10 w-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                                    <Mail className="h-5 w-5 text-indigo-400" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-400">Email us</p>
                                    <p className="text-white font-medium">hello@voiceagent.in</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="h-10 w-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                                    <Phone className="h-5 w-5 text-indigo-400" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-400">Call us</p>
                                    <p className="text-white font-medium">+91 98765 43210</p>
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="h-10 w-10 rounded-lg bg-indigo-500/10 flex items-center justify-center">
                                    <MapPin className="h-5 w-5 text-indigo-400" />
                                </div>
                                <div>
                                    <p className="text-sm text-gray-400">Location</p>
                                    <p className="text-white font-medium">Bengaluru, India</p>
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Right — Form */}
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                    >
                        {submitted ? (
                            <div className="bg-white/5 rounded-2xl border border-white/10 p-12 text-center">
                                <div className="h-16 w-16 rounded-full bg-green-500/10 flex items-center justify-center mx-auto mb-4">
                                    <Send className="h-8 w-8 text-green-400" />
                                </div>
                                <h3 className="text-xl font-semibold text-white">Thank you!</h3>
                                <p className="mt-2 text-gray-400">
                                    We&apos;ll reach out within 24 hours to schedule your demo.
                                </p>
                            </div>
                        ) : (
                            <form
                                onSubmit={handleSubmit}
                                className="bg-white/5 rounded-2xl border border-white/10 p-8 space-y-6"
                            >
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-300 mb-1.5">
                                            Name
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-2.5 text-white text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                                            placeholder="Rahul Sharma"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-gray-300 mb-1.5">
                                            Company
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-2.5 text-white text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                                            placeholder="Your D2C Brand"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-1.5">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        required
                                        className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-2.5 text-white text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                                        placeholder="rahul@brand.in"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-1.5">
                                        Monthly Support Volume
                                    </label>
                                    <select className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-2.5 text-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all">
                                        <option value="" className="bg-slate-900">Select range</option>
                                        <option value="<1k" className="bg-slate-900">&lt; 1,000 conversations</option>
                                        <option value="1-5k" className="bg-slate-900">1,000 – 5,000</option>
                                        <option value="5-10k" className="bg-slate-900">5,000 – 10,000</option>
                                        <option value="10k+" className="bg-slate-900">10,000+</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-1.5">
                                        Message (optional)
                                    </label>
                                    <textarea
                                        rows={3}
                                        className="w-full rounded-lg bg-white/5 border border-white/10 px-4 py-2.5 text-white text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all resize-none"
                                        placeholder="Tell us about your support challenges..."
                                    />
                                </div>

                                <button
                                    type="submit"
                                    className="w-full rounded-lg bg-indigo-500 px-6 py-3 text-sm font-semibold text-white hover:bg-indigo-400 transition-colors flex items-center justify-center gap-2"
                                >
                                    <Send className="h-4 w-4" /> Book a Demo
                                </button>
                            </form>
                        )}
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
