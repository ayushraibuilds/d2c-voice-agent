"use client";

import { useEffect, useState } from "react";
import {
  MessageSquare,
  TicketCheck,
  Users,
  Package,
  TrendingUp,
  Clock,
} from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Stats {
  total_messages: number;
  total_tickets: number;
  open_tickets: number;
  total_orders: number;
  unique_customers: number;
  messages_last_24h: number;
  intent_breakdown: Record<string, number>;
  lang_breakdown: Record<string, number>;
}

const INTENT_COLORS: Record<string, string> = {
  ORDER_STATUS: "bg-blue-500",
  REFUND_REQUEST: "bg-amber-500",
  ORDER_CANCEL: "bg-red-500",
  EXCHANGE_REQUEST: "bg-purple-500",
  PAYMENT_ISSUE: "bg-orange-500",
  DELIVERY_COMPLAINT: "bg-rose-500",
  PRODUCT_FAQ: "bg-cyan-500",
  HUMAN_HANDOFF: "bg-yellow-500",
  GREETING: "bg-green-500",
  UNKNOWN: "bg-gray-500",
};

export default function AdminDashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/stats`)
      .then((r) => r.json())
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-400">Could not load stats. Is the backend running?</p>
        <p className="text-sm text-gray-500 mt-2">
          Expected at <code className="text-indigo-400">{API_BASE}</code>
        </p>
      </div>
    );
  }

  const cards = [
    { label: "Total Messages", value: stats.total_messages, icon: MessageSquare, color: "text-blue-400" },
    { label: "Last 24 Hours", value: stats.messages_last_24h, icon: Clock, color: "text-cyan-400" },
    { label: "Unique Customers", value: stats.unique_customers, icon: Users, color: "text-green-400" },
    { label: "Total Orders", value: stats.total_orders, icon: Package, color: "text-amber-400" },
    { label: "Open Tickets", value: stats.open_tickets, icon: TicketCheck, color: "text-red-400" },
    { label: "Total Tickets", value: stats.total_tickets, icon: TrendingUp, color: "text-purple-400" },
  ];

  const totalIntents = Object.values(stats.intent_breakdown).reduce((a, b) => a + b, 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400 mt-1">Agent performance overview</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {cards.map((card) => (
          <div
            key={card.label}
            className="bg-white/5 rounded-xl border border-white/10 p-5 hover:bg-white/[.07] transition-colors"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">{card.label}</p>
                <p className="text-2xl font-bold text-white mt-1">
                  {card.value.toLocaleString()}
                </p>
              </div>
              <card.icon className={`h-8 w-8 ${card.color} opacity-50`} />
            </div>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Intent Breakdown */}
        <div className="bg-white/5 rounded-xl border border-white/10 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Intent Breakdown</h3>
          {Object.entries(stats.intent_breakdown).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(stats.intent_breakdown).map(([intent, count]) => (
                <div key={intent} className="flex items-center gap-3">
                  <div className={`h-3 w-3 rounded-full ${INTENT_COLORS[intent] || "bg-gray-500"}`} />
                  <span className="text-sm text-gray-300 w-40 truncate">{intent}</span>
                  <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${INTENT_COLORS[intent] || "bg-gray-500"}`}
                      style={{ width: `${(count / totalIntents) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-400 w-10 text-right">{count}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No data yet. Start some conversations!</p>
          )}
        </div>

        {/* Language Breakdown */}
        <div className="bg-white/5 rounded-xl border border-white/10 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Language Distribution</h3>
          {Object.entries(stats.lang_breakdown).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(stats.lang_breakdown).map(([lang, count]) => {
                const langNames: Record<string, string> = {
                  en: "English",
                  hi: "Hindi",
                  ta: "Tamil",
                  te: "Telugu",
                  kn: "Kannada",
                  bn: "Bengali",
                };
                return (
                  <div key={lang} className="flex items-center gap-3">
                    <span className="text-sm text-gray-300 w-20">{langNames[lang] || lang}</span>
                    <div className="flex-1 bg-white/10 rounded-full h-2 overflow-hidden">
                      <div
                        className="h-full rounded-full bg-indigo-500"
                        style={{
                          width: `${(count / Math.max(...Object.values(stats.lang_breakdown))) * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-sm text-gray-400 w-10 text-right">{count}</span>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-sm text-gray-500">No data yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}
