'use client';

import { useState } from 'react';
import { LayoutDashboard, Users, MessageSquare, TicketIcon, Settings, Search, Download, BarChart3, Clock, Bot } from 'lucide-react';
import Link from 'next/link';

// The components IntentBar, StatCard, NavItem should exist in src/components.
// Using inline implementations here for completeness in the page.

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col h-screen sticky top-0">
        <div className="p-6 border-b border-slate-800">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-indigo-500 rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold tracking-tight">Acme D2C</span>
          </Link>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          <LocalNavItem active={activeTab === 'overview'} onClick={() => setActiveTab('overview')} icon={<LayoutDashboard />} label="Overview" />
          <LocalNavItem active={activeTab === 'conversations'} onClick={() => setActiveTab('conversations')} icon={<MessageSquare />} label="Conversations" />
          <LocalNavItem active={activeTab === 'tickets'} onClick={() => setActiveTab('tickets')} icon={<TicketIcon />} label="Support Tickets" />
          <LocalNavItem active={activeTab === 'customers'} onClick={() => setActiveTab('customers')} icon={<Users />} label="Customers" />
          <LocalNavItem active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} icon={<Settings />} label="Brand Settings" />
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="bg-white border-b border-slate-200 px-8 py-5 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-2xl font-bold text-slate-800 capitalize">{activeTab}</h1>
          <div className="flex items-center gap-4">
            <button className="p-2 text-slate-400 hover:text-slate-600 transition bg-slate-100 rounded-full">
              <Search className="w-5 h-5" />
            </button>
            <div className="w-10 h-10 bg-indigo-100 text-indigo-700 font-bold rounded-full flex items-center justify-center border-2 border-indigo-200">
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
                <div className="col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                  <h3 className="text-lg font-bold text-slate-800 mb-6 flex justify-between items-center">
                    Message Volume
                    <span className="text-sm font-medium text-slate-500 bg-slate-100 px-3 py-1 rounded-full">Last 7 Days</span>
                  </h3>
                  <div className="h-64 flex items-end justify-between gap-2">
                    {[30, 45, 25, 60, 80, 50, 95].map((h, i) => (
                      <div key={i} className="w-full bg-indigo-100 rounded-t-md relative group">
                        <div 
                          className="absolute bottom-0 w-full bg-indigo-500 rounded-t-md transition-all duration-500 group-hover:bg-indigo-600"
                          style={{ height: `${h}%` }}
                        ></div>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between mt-4 text-xs font-medium text-slate-400">
                    <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                  <h3 className="text-lg font-bold text-slate-800 mb-6">Top Intents</h3>
                  <div className="space-y-5">
                    <LocalIntentBar label="Where is my order?" percent={45} color="bg-indigo-500" />
                    <LocalIntentBar label="Return / Refund" percent={25} color="bg-rose-500" />
                    <LocalIntentBar label="Product Enquiry" percent={15} color="bg-emerald-500" />
                    <LocalIntentBar label="Cancel Order" percent={10} color="bg-amber-500" />
                    <LocalIntentBar label="Talk to Human" percent={5} color="bg-slate-400" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'conversations' && (
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                <div className="relative w-64">
                  <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                  <input type="text" placeholder="Search by phone..." className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:ring-2 focus:ring-indigo-500" />
                </div>
                <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 text-slate-700 text-sm font-medium rounded-lg hover:bg-slate-50 transition">
                  <Download className="w-4 h-4" /> Export CSV
                </button>
              </div>
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-slate-500 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Customer</th>
                    <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Last Intent</th>
                    <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Language</th>
                    <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs">Time</th>
                    <th className="px-6 py-4 font-semibold uppercase tracking-wider text-xs text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {[
                    { phone: '+91 98765 43210', intent: 'track_order', lang: 'English', time: '2 mins ago' },
                    { phone: '+91 99887 76655', intent: 'refund_status', lang: 'Hindi (VOICE)', time: '15 mins ago' },
                    { phone: '+91 88776 65544', intent: 'talk_to_human', lang: 'Hinglish', time: '1 hour ago' },
                  ].map((row, i) => (
                    <tr key={i} className="hover:bg-slate-50 transition cursor-pointer group">
                      <td className="px-6 py-4 font-medium text-indigo-600">{row.phone}</td>
                      <td className="px-6 py-4 text-slate-700">
                        <span className="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-[4px] text-xs font-bold font-mono border border-slate-200">
                          {row.intent}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-500">{row.lang}</td>
                      <td className="px-6 py-4 text-slate-400">{row.time}</td>
                      <td className="px-6 py-4 text-right">
                        <span className="text-indigo-600 text-sm font-medium opacity-0 group-hover:opacity-100 transition">View Transcript &rarr;</span>
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
          ? 'bg-indigo-600 text-white font-medium' 
          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800 font-medium'
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
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">{icon}</div>
        <span className={`text-xs font-bold px-2 py-1 rounded-full ${isPos ? 'text-emerald-700 bg-emerald-50 border border-emerald-100' : 'text-rose-700 bg-rose-50 border border-rose-100'}`}>
          {change}
        </span>
      </div>
      <h4 className="text-slate-500 text-sm font-semibold mb-1 uppercase tracking-wider">{title}</h4>
      <div className="text-3xl font-bold text-slate-900">{value}</div>
    </div>
  );
}

function LocalIntentBar({ label, percent, color }: { label: string, percent: number, color: string }) {
  return (
    <div>
      <div className="flex justify-between text-sm font-medium mb-1.5">
        <span className="text-slate-700">{label}</span>
        <span className="text-slate-500">{percent}%</span>
      </div>
      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
        <div className={`h-2 rounded-full ${color}`} style={{ width: `${percent}%` }}></div>
      </div>
    </div>
  );
}
