import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "D2C Voice Agent — AI-Powered WhatsApp Support for Indian Brands",
  description:
    "Enterprise-grade voice-first WhatsApp AI support agent for Indian D2C brands. Handles Hinglish voice notes, order tracking, refunds, and smart human handoff.",
  keywords: [
    "D2C",
    "WhatsApp AI",
    "voice agent",
    "customer support",
    "India",
    "ONDC",
    "Shopify",
    "Hinglish",
  ],
  openGraph: {
    title: "D2C Voice Agent — AI WhatsApp Support",
    description:
      "Voice-first customer support that understands Hindi, Hinglish, and regional languages.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
