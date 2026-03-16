"use client";

import { motion } from "framer-motion";

const integrations = [
    {
        name: "ONDC",
        desc: "Open Network for Digital Commerce",
        gradient: "from-blue-600 to-blue-800",
        letter: "O",
    },
    {
        name: "Shopify",
        desc: "E-commerce Platform",
        gradient: "from-green-500 to-green-700",
        letter: "S",
    },
    {
        name: "Twilio",
        desc: "WhatsApp Business API",
        gradient: "from-red-500 to-red-700",
        letter: "T",
    },
    {
        name: "Groq",
        desc: "LPU Inference Engine",
        gradient: "from-orange-500 to-amber-600",
        letter: "G",
    },
    {
        name: "LangGraph",
        desc: "AI Orchestration",
        gradient: "from-purple-500 to-violet-700",
        letter: "L",
    },
    {
        name: "Zendesk",
        desc: "Help Desk Integration",
        gradient: "from-teal-500 to-cyan-700",
        letter: "Z",
    },
];

export function Integrations() {
    return (
        <section id="integrations" className="bg-slate-950 py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-base font-semibold text-indigo-400">Integrations</h2>
                    <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        Built on industry-leading platforms
                    </p>
                    <p className="mt-4 text-gray-400">
                        Plugs directly into your existing e-commerce and support stack.
                    </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6 max-w-4xl mx-auto">
                    {integrations.map((item, index) => (
                        <motion.div
                            key={item.name}
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.4, delay: index * 0.08 }}
                            className="flex flex-col items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10 hover:border-indigo-500/30 hover:bg-white/[.07] transition-all duration-300 cursor-default"
                        >
                            <div
                                className={`h-12 w-12 rounded-xl bg-gradient-to-br ${item.gradient} flex items-center justify-center shadow-lg`}
                            >
                                <span className="text-white font-bold text-lg">{item.letter}</span>
                            </div>
                            <div className="text-center">
                                <p className="text-sm font-semibold text-white">{item.name}</p>
                                <p className="text-xs text-gray-500 mt-0.5">{item.desc}</p>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
