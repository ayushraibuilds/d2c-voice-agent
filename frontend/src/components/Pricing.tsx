"use client";

import { motion } from "framer-motion";
import { Check, Sparkles } from "lucide-react";

const plans = [
    {
        name: "Starter",
        price: "₹4,999",
        period: "/mo",
        description: "For small D2C brands getting started with AI support.",
        features: [
            "Up to 1,000 conversations/month",
            "WhatsApp voice + text support",
            "5 languages supported",
            "Order tracking integration",
            "Email support",
        ],
        cta: "Start Free Trial",
        popular: false,
    },
    {
        name: "Growth",
        price: "₹14,999",
        period: "/mo",
        description: "For scaling brands with high support volume.",
        features: [
            "Up to 10,000 conversations/month",
            "Everything in Starter, plus:",
            "ONDC + Shopify integration",
            "Custom FAQ knowledge base",
            "Zendesk/Freshdesk handoff",
            "Analytics dashboard",
            "Priority support",
        ],
        cta: "Start Free Trial",
        popular: true,
    },
    {
        name: "Enterprise",
        price: "Custom",
        period: "",
        description: "For large operations needing custom solutions.",
        features: [
            "Unlimited conversations",
            "Everything in Growth, plus:",
            "Multi-brand support",
            "Custom LLM fine-tuning",
            "Dedicated account manager",
            "SLA guarantees",
            "On-premise deployment option",
        ],
        cta: "Contact Sales",
        popular: false,
    },
];

export function Pricing() {
    return (
        <section id="pricing" className="bg-slate-900 py-24 sm:py-32">
            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl text-center mb-16">
                    <h2 className="text-base font-semibold text-indigo-400">Pricing</h2>
                    <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        Plans that scale with your brand
                    </p>
                    <p className="mt-4 text-gray-400">
                        Start free. No credit card required. Cancel anytime.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                    {plans.map((plan, index) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.5, delay: index * 0.1 }}
                            className={`relative rounded-2xl p-8 ${
                                plan.popular
                                    ? "bg-gradient-to-b from-indigo-500/10 to-transparent border-2 border-indigo-500/50 shadow-xl shadow-indigo-500/10"
                                    : "bg-white/5 border border-white/10"
                            }`}
                        >
                            {plan.popular && (
                                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                                    <span className="inline-flex items-center gap-1 rounded-full bg-indigo-500 px-3 py-1 text-xs font-semibold text-white">
                                        <Sparkles className="h-3 w-3" /> Most Popular
                                    </span>
                                </div>
                            )}

                            <h3 className="text-lg font-semibold text-white">{plan.name}</h3>
                            <p className="mt-1 text-sm text-gray-400">{plan.description}</p>

                            <div className="mt-6 flex items-baseline gap-1">
                                <span className="text-4xl font-bold text-white">{plan.price}</span>
                                <span className="text-gray-400">{plan.period}</span>
                            </div>

                            <a
                                href="#contact"
                                className={`mt-6 block w-full rounded-lg py-2.5 text-center text-sm font-semibold transition-colors ${
                                    plan.popular
                                        ? "bg-indigo-500 text-white hover:bg-indigo-400"
                                        : "bg-white/10 text-white hover:bg-white/20"
                                }`}
                            >
                                {plan.cta}
                            </a>

                            <ul className="mt-8 space-y-3">
                                {plan.features.map((feature) => (
                                    <li key={feature} className="flex items-start gap-3 text-sm text-gray-300">
                                        <Check className="h-4 w-4 text-indigo-400 shrink-0 mt-0.5" />
                                        {feature}
                                    </li>
                                ))}
                            </ul>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
