"use client";

import { useEffect, useState } from "react";
import { CheckCircle, AlertCircle, Clock } from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Ticket {
  ticket_id: string;
  phone: string;
  message: string;
  intent: string;
  status: string;
  created_at: string;
}

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [closing, setClosing] = useState<string | null>(null);

  useEffect(() => {
    const fetchTickets = () => {
      setLoading(true);
      fetch(`${API_BASE}/api/v1/tickets`)
        .then((r) => r.json())
        .then((d) => setTickets(d.tickets || []))
        .catch(console.error)
        .finally(() => setLoading(false));
    };

    fetchTickets();
  }, []);

  const handleRefresh = () => {
    setLoading(true);
    fetch(`${API_BASE}/api/v1/tickets`)
      .then((r) => r.json())
      .then((d) => setTickets(d.tickets || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  const closeTicket = (ticketId: string) => {
    setClosing(ticketId);
    fetch(`${API_BASE}/api/v1/tickets/${ticketId}/close`, { method: "POST" })
      .then((r) => {
        if (r.ok) {
          setTickets((prev) => prev.filter((t) => t.ticket_id !== ticketId));
        }
      })
      .catch(console.error)
      .finally(() => setClosing(null));
  };

  const intentColors: Record<string, string> = {
    HUMAN_HANDOFF: "text-yellow-400 bg-yellow-400/10",
    DELIVERY_COMPLAINT: "text-red-400 bg-red-400/10",
    PAYMENT_ISSUE: "text-orange-400 bg-orange-400/10",
    EXCHANGE_REQUEST: "text-purple-400 bg-purple-400/10",
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Tickets</h1>
          <p className="text-gray-400 mt-1">
            {tickets.length} open ticket{tickets.length !== 1 ? "s" : ""}
          </p>
        </div>
        <button
          onClick={handleRefresh}
          className="text-sm text-gray-400 hover:text-white px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 transition-all"
        >
          Refresh
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="h-8 w-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : tickets.length === 0 ? (
        <div className="bg-white/5 rounded-xl border border-white/10 p-12 text-center">
          <CheckCircle className="h-12 w-12 text-green-400 mx-auto mb-4 opacity-50" />
          <p className="text-lg font-medium text-white">All clear!</p>
          <p className="text-sm text-gray-400 mt-1">No open tickets right now.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tickets.map((ticket) => (
            <div
              key={ticket.ticket_id}
              className="bg-white/5 rounded-xl border border-white/10 p-5 hover:bg-white/[.07] transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-sm font-mono font-medium text-indigo-400">
                      {ticket.ticket_id}
                    </span>
                    <span
                      className={`text-[11px] px-2 py-0.5 rounded-full font-medium ${
                        intentColors[ticket.intent] || "text-gray-400 bg-white/10"
                      }`}
                    >
                      {ticket.intent}
                    </span>
                  </div>

                  <p className="text-sm text-gray-300 break-words">{ticket.message}</p>

                  <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                    <span className="flex items-center gap-1">
                      <AlertCircle className="h-3 w-3" />
                      {ticket.phone}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {new Date(ticket.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => closeTicket(ticket.ticket_id)}
                  disabled={closing === ticket.ticket_id}
                  className="shrink-0 mt-1 text-sm px-3 py-1.5 rounded-lg bg-green-500/10 text-green-400 hover:bg-green-500/20 border border-green-500/20 transition-all disabled:opacity-50"
                >
                  {closing === ticket.ticket_id ? "Closing..." : "Close"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
