"use client";

import { useEffect, useState } from "react";
import { MessageSquare, Search, ArrowRight } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Customer {
  phone: string;
  message: string;
  intent: string;
  created_at: string;
  msg_count: number;
}

interface Message {
  role: string;
  message: string;
  intent: string;
  detected_lang: string;
  created_at: string;
}

export default function ConversationsPage() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [selectedPhone, setSelectedPhone] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/customers`)
      .then((r) => r.json())
      .then((d) => setCustomers(d.customers || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const loadMessages = (phone: string) => {
    setSelectedPhone(phone);
    fetch(`${API_BASE}/api/v1/conversations/${encodeURIComponent(phone)}?limit=50`)
      .then((r) => r.json())
      .then((d) => setMessages(d.messages || []));
  };

  const filtered = customers.filter(
    (c) =>
      c.phone.includes(search) ||
      c.message.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Conversations</h1>
        <p className="text-gray-400 mt-1">Browse customer interactions</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-220px)]">
        {/* Customer List */}
        <div className="bg-white/5 rounded-xl border border-white/10 flex flex-col overflow-hidden">
          <div className="p-4 border-b border-white/10">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
              <input
                type="text"
                placeholder="Search by phone or message..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="h-6 w-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
              </div>
            ) : filtered.length === 0 ? (
              <p className="text-center text-sm text-gray-500 py-12">No conversations found</p>
            ) : (
              filtered.map((c) => (
                <button
                  key={c.phone}
                  onClick={() => loadMessages(c.phone)}
                  className={`w-full text-left p-4 border-b border-white/5 hover:bg-white/5 transition-colors ${
                    selectedPhone === c.phone ? "bg-indigo-500/10 border-l-2 border-l-indigo-500" : ""
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-white truncate">{c.phone}</span>
                    <span className="text-xs text-gray-500">{c.msg_count} msgs</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1 truncate">{c.message}</p>
                  {c.intent && (
                    <span className="inline-block mt-1 text-[10px] px-1.5 py-0.5 rounded bg-white/10 text-gray-300">
                      {c.intent}
                    </span>
                  )}
                </button>
              ))
            )}
          </div>
        </div>

        {/* Message Thread */}
        <div className="lg:col-span-2 bg-white/5 rounded-xl border border-white/10 flex flex-col overflow-hidden">
          {selectedPhone ? (
            <>
              <div className="p-4 border-b border-white/10 flex items-center gap-3">
                <MessageSquare className="h-5 w-5 text-indigo-400" />
                <span className="text-white font-medium">{selectedPhone}</span>
                <span className="text-xs text-gray-500">{messages.length} messages</span>
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`flex ${msg.role === "user" ? "justify-start" : "justify-end"}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-xl px-4 py-2.5 ${
                        msg.role === "user"
                          ? "bg-white/10 text-gray-200"
                          : "bg-indigo-500/20 text-gray-200"
                      }`}
                    >
                      <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] text-gray-500">
                          {new Date(msg.created_at).toLocaleString()}
                        </span>
                        {msg.intent && (
                          <span className="text-[10px] px-1 rounded bg-white/10 text-gray-400">
                            {msg.intent}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <ArrowRight className="h-8 w-8 text-gray-600 mx-auto mb-3" />
                <p className="text-gray-400">Select a conversation to view</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
