"use client";

import { motion } from "framer-motion";
import { Mic, Play, CheckCheck, Link as LinkIcon } from "lucide-react";
import { useEffect, useState } from "react";

export function InteractiveChat() {
    const [step, setStep] = useState(0);

    useEffect(() => {
        // Sequence the chat animations
        const timer1 = setTimeout(() => setStep(1), 1000); // Show voice note
        const timer2 = setTimeout(() => setStep(2), 2500); // Show typing...
        const timer3 = setTimeout(() => setStep(3), 4000); // Show AI response

        return () => {
            clearTimeout(timer1);
            clearTimeout(timer2);
            clearTimeout(timer3);
        };
    }, []);

    return (
        <section className="bg-slate-900 py-24 sm:py-32 overflow-hidden">
            <div className="mx-auto max-w-7xl px-6 lg:px-8 flex flex-col items-center">
                <div className="text-center mb-16">
                    <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                        See it in Action
                    </h2>
                    <p className="mt-4 text-lg text-gray-400">
                        Real-time Hinglish voice transcription and intent routing.
                    </p>
                </div>

                {/* Mock WhatsApp UI */}
                <div className="w-full max-w-md bg-[#efeae2] rounded-3xl overflow-hidden shadow-2xl ring-1 ring-white/10 relative">

                    {/* Header */}
                    <div className="bg-[#075e54] px-4 py-3 flex items-center gap-3">
                        <div className="h-10 w-10 bg-indigo-500 rounded-full flex items-center justify-center text-white font-bold">
                            AI
                        </div>
                        <div>
                            <h3 className="text-white font-medium">D2C Support Bot</h3>
                            <p className="text-green-100 text-xs mt-0.5">
                                {step === 2 ? "typing..." : "online"}
                            </p>
                        </div>
                    </div>

                    {/* Chat Canvas */}
                    <div className="p-4 space-y-4 h-[400px] overflow-y-auto bg-[url('https://wallpapers.com/images/hd/whatsapp-chat-background-030a0hnhgyfbgpmv.jpg')] bg-cover bg-center">

                        {/* User Voice Note Element */}
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{
                                opacity: step >= 1 ? 1 : 0,
                                scale: step >= 1 ? 1 : 0.9,
                                y: step >= 1 ? 0 : 20
                            }}
                            transition={{ type: "spring", bounce: 0.4 }}
                            className="flex justify-end"
                        >
                            <div className="bg-[#dcf8c6] px-3 py-2 rounded-lg rounded-tr-none max-w-[85%] shadow-sm flex items-center gap-3">
                                <button className="h-8 w-8 bg-green-500 rounded-full flex items-center justify-center text-white shrink-0">
                                    <Play className="h-4 w-4 ml-0.5" />
                                </button>
                                <div className="flex-1">
                                    <div className="flex items-center h-4 gap-[2px]">
                                        {[...Array(15)].map((_, i) => (
                                            <motion.div
                                                key={i}
                                                animate={step === 1 ? {
                                                    height: ["20%", "100%", "20%"]
                                                } : { height: "20%" }}
                                                transition={{
                                                    repeat: Infinity,
                                                    duration: 1.2,
                                                    delay: i * 0.1
                                                }}
                                                className="w-1 bg-green-600/40 rounded-full"
                                            />
                                        ))}
                                    </div>
                                </div>
                                <div className="flex items-end self-end gap-1 mb-[-4px]">
                                    <span className="text-[10px] text-gray-500">10:42 AM</span>
                                    <CheckCheck className="h-3 w-3 text-blue-500" />
                                </div>
                            </div>
                        </motion.div>

                        {/* AI Response Element */}
                        {step >= 3 && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.9, x: -20 }}
                                animate={{ opacity: 1, scale: 1, x: 0 }}
                                transition={{ type: "spring", bounce: 0.4 }}
                                className="flex justify-start"
                            >
                                <div className="bg-white px-3 py-2 rounded-lg rounded-tl-none max-w-[85%] shadow-sm">
                                    <p className="text-[#303030] text-[14px] leading-snug">
                                        <span className="text-gray-500 italic text-xs block mb-1">
                                            🗣️ &quot;Mera order kahan hai?&quot;
                                        </span>
                                        📦 आपका ऑडर <strong>ORD-12345</strong> अभी &apos;Out for Delivery&apos; है। इसके आज रात 8 बजे तक पहुंचने की उम्मीद है।
                                    </p>

                                    <div className="mt-2 p-2 bg-gray-50 rounded border border-gray-100 flex items-center gap-2 cursor-pointer hover:bg-gray-100 transition-colors">
                                        <div className="h-8 w-8 bg-indigo-100 rounded flex items-center justify-center text-indigo-600 shrink-0">
                                            <LinkIcon className="h-4 w-4" />
                                        </div>
                                        <div className="overflow-hidden">
                                            <p className="text-sm font-medium text-gray-900 truncate">Track Order Flow</p>
                                            <p className="text-xs text-gray-500 truncate">track.d2cbrand.in/ord-12345</p>
                                        </div>
                                    </div>

                                    <div className="flex justify-end mt-1">
                                        <span className="text-[10px] text-gray-400">10:42 AM</span>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="bg-[#f0f0f0] px-3 py-3 flex items-center gap-2">
                        <div className="flex-1 bg-white rounded-full h-10 px-4 flex items-center text-gray-400 text-sm shadow-sm">
                            Type a message
                        </div>
                        <div className="h-10 w-10 bg-[#00a884] rounded-full flex items-center justify-center text-white shadow-sm">
                            <Mic className="h-5 w-5" />
                        </div>
                    </div>
                </div>

                {/* Replay Button */}
                <button
                    onClick={() => setStep(0)}
                    className="mt-8 text-sm text-indigo-400 hover:text-indigo-300 transition-colors flex items-center gap-2"
                >
                    Replay Animation
                </button>

            </div>
        </section>
    );
}
