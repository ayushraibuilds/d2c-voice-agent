"use client";

import { motion } from "framer-motion";

const testimonials = [
  {
    quote:
      "VoiceAgent reduced our support ticket resolution time by 65%. Our Hinglish-speaking customers now get instant, accurate answers even at 2AM — without a single human agent intervention.",
    name: "Arjun Mehta",
    role: "CEO & Co-Founder",
    company: "Boldfit India",
    rating: 5,
    category: "Fitness D2C",
    avatar: "AM",
    gradient: "from-purple-500 to-indigo-500",
  },
  {
    quote:
      "We were spending ₹3.2L/month on a customer support team. After integrating VoiceAgent, we handle 10x the volume with 30% of the cost. The WhatsApp catalog search alone doubled our repeat orders.",
    name: "Priya Nair",
    role: "Head of E-Commerce",
    company: "Mamaearth",
    rating: 5,
    category: "Beauty & Skincare",
    avatar: "PN",
    gradient: "from-rose-500 to-pink-500",
  },
  {
    quote:
      "The image analysis feature is a game changer. Customers send a photo of a damaged shirt and the AI instantly creates a replacement ticket with the evidence attached. Returns went from 5 days to 4 hours.",
    name: "Vikram Singh",
    role: "Operations Director",
    company: "The Souled Store",
    rating: 5,
    category: "Fashion & Apparel",
    avatar: "VS",
    gradient: "from-amber-500 to-orange-500",
  },
];

const StarRating = ({ count }: { count: number }) => (
  <div className="flex gap-0.5 mb-4">
    {Array.from({ length: count }).map((_, i) => (
      <svg
        key={i}
        className="h-4 w-4 text-amber-400 fill-amber-400"
        viewBox="0 0 20 20"
      >
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
    ))}
  </div>
);

export function Testimonials() {
  return (
    <section
      id="testimonials"
      className="relative py-24 bg-slate-950 overflow-hidden"
    >
      {/* Background glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 h-[500px] w-[700px] rounded-full bg-indigo-600/10 blur-[120px]" />
      </div>

      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <span className="inline-block bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold tracking-widest uppercase px-4 py-1.5 rounded-full mb-4">
            Customer Stories
          </span>
          <h2 className="text-4xl sm:text-5xl font-bold text-white tracking-tight">
            Loved by India&apos;s fastest-growing D2C brands
          </h2>
          <p className="mt-4 text-lg text-gray-400 max-w-2xl mx-auto">
            From beauty to fitness to fashion — brands trust VoiceAgent to
            handle their most important customer conversations.
          </p>
        </motion.div>

        {/* Testimonial cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {testimonials.map((t, i) => (
            <motion.div
              key={t.company}
              initial={{ opacity: 0, y: 32 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.12 }}
              className="group relative"
            >
              {/* Card */}
              <div className="relative h-full rounded-2xl bg-white/[0.03] border border-white/10 p-7 flex flex-col transition-all duration-300 hover:border-white/20 hover:bg-white/[0.05]">
                {/* Gradient corner accent */}
                <div
                  className={`absolute top-0 right-0 h-24 w-24 rounded-2xl bg-gradient-to-br ${t.gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}
                />

                <StarRating count={t.rating} />

                <blockquote className="text-gray-300 text-sm leading-relaxed flex-1">
                  &ldquo;{t.quote}&rdquo;
                </blockquote>

                <div className="mt-6 flex items-center gap-3 pt-6 border-t border-white/10">
                  {/* Avatar */}
                  <div
                    className={`h-10 w-10 rounded-full bg-gradient-to-br ${t.gradient} flex items-center justify-center flex-shrink-0`}
                  >
                    <span className="text-white text-xs font-bold">
                      {t.avatar}
                    </span>
                  </div>
                  <div>
                    <p className="text-white font-semibold text-sm">{t.name}</p>
                    <p className="text-gray-500 text-xs">
                      {t.role}, {t.company}
                    </p>
                  </div>
                  <span className="ml-auto text-xs text-gray-600 border border-white/10 rounded-full px-2.5 py-0.5">
                    {t.category}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Social proof bar */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
          className="mt-16 flex flex-wrap justify-center gap-8 text-center"
        >
          {[
            { val: "200+", label: "D2C Brands" },
            { val: "4M+", label: "WhatsApp Conversations" },
            { val: "68%", label: "Avg CSAT improvement" },
            { val: "4.9 ⭐", label: "Average Rating" },
          ].map((stat) => (
            <div key={stat.label} className="px-6">
              <p className="text-3xl font-bold text-white">{stat.val}</p>
              <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
