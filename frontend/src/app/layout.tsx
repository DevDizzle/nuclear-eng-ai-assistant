import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { FileText, MessageSquare, ShieldAlert, LayoutDashboard } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Nuclear Eng AI Assistant",
  description: "RAG-powered document assistant for nuclear engineers",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex h-screen bg-gray-50 text-gray-900`}>
        {/* Sidebar */}
        <aside className="w-64 bg-gray-900 text-white flex flex-col hidden md:flex">
          <div className="p-4 text-xl font-bold border-b border-gray-800 flex items-center gap-2">
            <ShieldAlert className="text-amber-500" />
            <span>Nuclear AI</span>
          </div>
          <nav className="flex-1 p-4 space-y-2">
            <Link href="/" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition">
              <LayoutDashboard size={20} /> Dashboard
            </Link>
            <Link href="/documents" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition">
              <FileText size={20} /> Documents
            </Link>
            <Link href="/query" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition">
              <MessageSquare size={20} /> Q&A Chat
            </Link>
            <Link href="/screening" className="flex items-center gap-3 p-2 rounded hover:bg-gray-800 transition">
              <ShieldAlert size={20} /> 50.59 Screening
            </Link>
          </nav>
        </aside>
        
        {/* Main Content */}
        <main className="flex-1 flex flex-col overflow-hidden bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  );
}