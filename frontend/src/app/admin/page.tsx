'use client';

import { useState } from 'react';
import { LayoutDashboard, Users, MessageSquare, TicketIcon, Settings, Search, Download, BarChart3, Clock, Bot } from 'lucide-react';
import Link from 'next/link';

// The components IntentBar, StatCard, NavItem should exist in src/components.
// Using inline implementations here for completeness in the page.

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-black text-slate-200 flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#0a0a0c] text-white flex flex-col h-screen sticky top-0 border-r border-white/5 z-20">
        <div className="p-6 border-b border-white/5">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(99,102,241,0.5)]">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">Acme D2C</span>
          </Link>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <LocalNavItem active={activeTab === 'overview'} onClick={() => setActiveTab('overview')} icon={<LayoutDashboard />} label="Overview" />
          <LocalNavItem active={activeTab === 'conversations'} onClick={() => setActiveTab('conversations')} icon={<MessageSquare />} label="Conversations" />
          <LocalNavItem active={activeTab === 'tickets'} onClick={() => setActiveTab('tickets')} icon={<TicketIcon />} label="Support Tickets" />
          <LocalNavItem active={activeTab === 'customers'} onClick={() => setActiveTab('customers')} icon={<Users />} label="Customers" />
          <LocalNavItem active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} icon={<Settings />} label="Brand Settings" />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-black relative">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-900/20 rounded-full blur-[120px] pointer-events-none"></div>
        <header className="bg-black/60 backdrop-blur-md border-b border-white/5 px-8 py-5 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-2xl font-bold text-white capitalize tracking-tight">{activeTab}</h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20 text-xs font-bold uppercase tracking-widest shadow-[0_0_10px_rgba(16,185,129,0.2)]">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Systems Operational
            </div>
            <button className="p-2 text-slate-400 hover:text-white transition bg-white/5 rounded-full border border-white/5 hover:border-white/10">
              <Search className="w-5 h-5" />
            </button>
            <div className="w-10 h-10 bg-indigo-500/10 text-indigo-400 font-bold rounded-full flex items-center justify-center border border-indigo-500/30 shadow-[0_0_15px_rgba(99,102,241,0.2)]">
              JS
            </div>
          </div>
        </header>

        <div className="p-8">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Stats Row */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <LocalStatCard title="Total Messages" value="12,450" change="+14%" icon={<MessageSquare />} />
                <LocalStatCard title="Active Tickets" value="24" change="-5%" icon={<TicketIcon />} />
                <LocalStatCard title="Resolution Time" value="4.2m" change="-1.2m" icon={<Clock />} />
                <LocalStatCard title="CSAT Score" value="4.8/5" change="+0.2" icon={<BarChart3 />} />
              </div>

              {/* Charts area mockup */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="col-span-2 bg-[#0a0a0c] p-6 rounded-2xl shadow-xl border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
                  <h3 className="text-lg font-bold text-white mb-6 flex justify-between items-center relative z-10">
                    Message Volume
                    <span className="text-xs font-bold text-slate-400 bg-white/5 px-3 py-1 rounded-full border border-white/5 tracking-widest uppercase">LAST 7 DAYS</span>
                  </h3>
                  <div className="h-64 flex items-end justify-between gap-2 relative z-10">
                    {[30, 45, 25, 60, 80, 50, 95].map((h, i) => (
                      <div key={i} className="w-full bg-indigo-950/30 rounded-t-md relative group/bar overflow-hidden shadow-inner border border-indigo-500/10">
                        <div 
                          className="absolute bottom-0 w-full bg-gradient-to-t from-indigo-600 to-indigo-400 rounded-t-md transition-all duration-500 group-hover/bar:from-indigo-500 group-hover/bar:to-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.4)]"
                          style={{ height: `${h}%` }}
                        ></div>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between mt-4 text-xs font-bold text-slate-500 tracking-widest relative z-10">
                    <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
                  </div>
                </div>

                <div className="bg-[#0a0a0c] p-6 rounded-2xl shadow-xl border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-fuchsia-500/10 blur-3xl rounded-full"></div>
                  <h3 className="text-lg font-bold text-white mb-6 relative z-10">Top Intents</h3>
                  <div className="space-y-6 relative z-10">
                    <LocalIntentBar label="Where is my order?" percent={45} color="bg-indigo-500" />
                    <LocalIntentBar label="Return / Refund" percent={25} color="bg-rose-500" />
                    <LocalIntentBar label="Product Enquiry" percent={15} color="bg-emerald-500" />
                    <LocalIntentBar label="Cancel Order" percent={10} color="bg-amber-500" />
                    <LocalIntentBar label="Talk to Human" percent={5} color="bg-slate-500" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'conversations' && (
            <div className="bg-[#0a0a0c] rounded-2xl shadow-xl border border-white/5 overflow-hidden">
              <div className="p-4 border-b border-white/5 flex justify-between items-center bg-white/5 backdrop-blur-md">
                <div className="relative w-64">
                  <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input type="text" placeholder="Search by phone..." className="w-full pl-9 pr-4 py-2 border border-white/10 bg-black/50 text-white rounded-lg text-sm outline-none focus:ring-2 focus:ring-indigo-500 shadow-inner" />
                </div>
                <button className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 text-slate-300 text-sm font-bold rounded-lg hover:bg-white/10 transition">
                  <Download className="w-4 h-4" /> Export CSV
                </button>
              </div>
              <table className="w-full text-left text-sm">
                <thead className="bg-black/40 text-slate-400 border-b border-white/5 shadow-sm">
                  <tr>
                    <th className="px-6 py-4 font-bold uppercase tracking-widest text-xs">Customer</th>
                    <th className="px-6 py-4 font-bold uppercase tracking-widest text-xs">Last Intent</th>
                    <th className="px-6 py-4 font-bold uppercase tracking-widest text-xs">Language</th>
                    <th className="px-6 py-4 font-bold uppercase tracking-widest text-xs">Time</th>
                    <th className="px-6 py-4 font-bold uppercase tracking-widest text-xs text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {[
                    { phone: '+91 98765 43210', intent: 'track_order', lang: 'English', time: '2 mins ago' },
                    { phone: '+91 99887 76655', intent: 'refund_status', lang: 'Hindi (VOICE)', time: '15 mins ago' },
                    { phone: '+91 88776 65544', intent: 'talk_to_human', lang: 'Hinglish', time: '1 hour ago' },
                  ].map((row, i) => (
                    <tr key={i} className="hover:bg-white/5 transition cursor-pointer group">
                      <td className="px-6 py-4 font-bold text-indigo-400">{row.phone}</td>
                      <td className="px-6 py-4 text-slate-300">
                        <span className="px-2.5 py-1 bg-slate-800 text-slate-300 rounded-[4px] text-xs font-bold font-mono border border-slate-700">
                          {row.intent}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-400 font-medium">{row.lang}</td>
                      <td className="px-6 py-4 text-slate-500 font-medium">{row.time}</td>
                      <td className="px-6 py-4 text-right">
                        <span className="text-indigo-400 text-sm font-bold opacity-0 group-hover:opacity-100 transition">View Transcript &rarr;</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

// Inline fallback UI components
function LocalNavItem({ icon, label, active, onClick }: { icon: React.ReactNode, label: string, active: boolean, onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition ${
        active 
          ? 'bg-indigo-600/20 text-indigo-400 font-bold border border-indigo-500/20 shadow-[0_0_15px_rgba(79,70,229,0.15)]' 
          : 'text-slate-400 hover:text-white hover:bg-white/5 font-medium border border-transparent'
      }`}
    >
      <div className="w-5 h-5">{icon}</div>
      <span>{label}</span>
    </button>
  );
}

function LocalStatCard({ title, value, change, icon }: { title: string, value: string, change: string, icon: React.ReactNode }) {
  const isPos = change.startsWith('+');
  return (
    <div className="bg-[#0a0a0c] p-6 rounded-2xl shadow-xl border border-white/5 relative overflow-hidden group hover:border-white/10 transition-colors">
      <div className="absolute -top-10 -right-10 w-32 h-32 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-colors"></div>
      <div className="flex justify-between items-start mb-4 relative z-10">
        <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20 shadow-inner">{icon}</div>
        <span className={`text-xs font-bold px-2 py-1 rounded-full ${isPos ? 'text-emerald-400 bg-emerald-500/10 border border-emerald-500/20' : 'text-rose-400 bg-rose-500/10 border border-rose-500/20'}`}>
          {change}
        </span>
      </div>
      <h4 className="text-slate-400 text-xs font-bold mb-1 uppercase tracking-widest relative z-10">{title}</h4>
      <div className="text-3xl font-extrabold text-white relative z-10">{value}</div>
    </div>
  );
}

function LocalIntentBar({ label, percent, color }: { label: string, percent: number, color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs font-bold mb-2 uppercase tracking-wide">
        <span className="text-slate-300">{label}</span>
        <span className="text-slate-400">{percent}%</span>
      </div>
      <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden shadow-inner">
        <div className={`h-1.5 rounded-full ${color} shadow-[0_0_10px_currentColor]`} style={{ width: `${percent}%` }}></div>
      </div>
    </div>
  );
}
