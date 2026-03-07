"use client";

import React, { useState } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import api from '@/lib/api';
import CitationTable from './CitationTable';

export default function ChatInterface() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.post('/query', { question: userMsg.content });
      setMessages((prev) => [
        ...prev, 
        { role: 'assistant', content: res.data.answer, citations: res.data.citations }
      ]);
    } catch (err) {
      console.error('Query failed', err);
      setMessages((prev) => [
        ...prev, 
        { role: 'assistant', content: 'An error occurred while generating the response.', citations: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-gray-400 text-center">
            <div>
              <Bot size={48} className="mx-auto mb-4 opacity-50" />
              <p>Ask a question about the uploaded engineering documents.</p>
              <p className="text-sm mt-2 max-w-sm">"What is the required flow rate for the auxiliary feedwater system?"</p>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`flex gap-4 ${msg.role === 'assistant' ? 'bg-gray-50 -mx-6 px-6 py-6 border-y border-gray-100' : ''}`}>
              <div className="flex-shrink-0">
                {msg.role === 'user' ? (
                  <div className="bg-blue-100 p-2 rounded-full text-blue-600">
                    <User size={20} />
                  </div>
                ) : (
                  <div className="bg-amber-100 p-2 rounded-full text-amber-600">
                    <Bot size={20} />
                  </div>
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="prose max-w-none text-gray-800 whitespace-pre-wrap">
                  {msg.content}
                </div>
                {msg.citations && msg.citations.length > 0 && (
                  <CitationTable citations={msg.citations} />
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex gap-4 bg-gray-50 -mx-6 px-6 py-6 border-y border-gray-100">
            <div className="bg-amber-100 p-2 rounded-full text-amber-600 flex-shrink-0 h-10">
              <Bot size={20} />
            </div>
            <div className="flex items-center text-gray-500">
              <Loader2 className="animate-spin mr-2" size={20} /> Analyzing documents...
            </div>
          </div>
        )}
      </div>
      <div className="p-4 border-t border-gray-200 bg-gray-50">
        <form onSubmit={sendMessage} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a technical question..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center w-12"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}