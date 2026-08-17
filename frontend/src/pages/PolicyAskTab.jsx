import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { askPolicyQuestionApi } from '../services/api';
import { MessageSquare, Send, Sparkles, AlertCircle, FileSearch, Flag, Check } from 'lucide-react';

export default function PolicyAskTab() {
  const { chatHistory, setChatHistory, t } = useApp();
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [feedbackText, setFeedbackText] = useState('');
  const [ticketCreated, setTicketCreated] = useState(null);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    const userMsg = { role: 'user', content: query };
    setChatHistory((prev) => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    try {
      const res = await askPolicyQuestionApi(userMsg.content, chatHistory);
      const assistantMsg = {
        role: 'assistant',
        content: res.answer,
        trace_id: res.trace_id,
      };
      setChatHistory((prev) => [...prev, assistantMsg]);
    } catch (err) {
      setChatHistory((prev) => [
        ...prev,
        { role: 'assistant', content: 'An error occurred while querying policy: ' + err.message }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleTicketSubmit = (e) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;

    const tkt = 'TKT-SUPP-' + Math.random().toString(36).substring(2, 10).toUpperCase();
    setTicketCreated(tkt);
    setFeedbackText('');
  };

  return (
    <div className="space-y-6">
      {/* Sub-limit and Procedure Quick Lookup */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-4">
        <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
          <FileSearch className="w-5 h-5 text-[#003178]" />
          Procedure-Specific Sub-Limit & Document Lookup
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-3 bg-gray-50 rounded border border-gray-200">
            <span className="font-semibold text-gray-500 block">Cataract Surgery Sub-Limit</span>
            <span className="text-sm font-bold text-gray-900">₹40,000 per eye</span>
          </div>
          <div className="p-3 bg-gray-50 rounded border border-gray-200">
            <span className="font-semibold text-gray-500 block">Joint Replacement Waiting Period</span>
            <span className="text-sm font-bold text-gray-900">24 Months Specific Exclusion</span>
          </div>
          <div className="p-3 bg-gray-50 rounded border border-gray-200">
            <span className="font-semibold text-gray-500 block">Day Care Procedure Eligibility</span>
            <span className="text-sm font-bold text-emerald-700">Covered (No 24h Mandatory Stay)</span>
          </div>
        </div>
      </div>

      {/* Main Q&A Chat Assistant */}
      <div className="bg-white rounded-lg border border-gray-200 shadow-sm flex flex-col h-[520px]">
        <div className="p-4 border-b border-gray-200 bg-gray-50 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-blue-800" />
            <h3 className="font-bold text-gray-900">{t.ask_header}</h3>
          </div>
          <span className="text-xs bg-blue-100 text-blue-800 font-semibold px-2.5 py-0.5 rounded-full">
            Real-Time Token Streaming Active
          </span>
        </div>

        {/* Message Log */}
        <div className="flex-1 p-4 overflow-y-auto space-y-4 text-sm">
          {chatHistory.map((msg, i) => (
            <div
              key={i}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-2xl rounded-lg p-4 space-y-1.5 ${
                  msg.role === 'user'
                    ? 'bg-[#003178] text-white'
                    : 'bg-blue-50/70 border border-blue-200 text-gray-800'
                }`}
              >
                <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                {msg.trace_id && (
                  <div className="text-[10px] text-blue-600 font-mono pt-1 border-t border-blue-200/50">
                    RAG Audit Trace ID: {msg.trace_id} | Groq Llama-3.3-70B Engine
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-xs text-blue-800 font-medium p-3 bg-blue-50 rounded">
              <Sparkles className="w-4 h-4 animate-spin text-blue-700" />
              <span>Searching policy vector chunks and streaming answer...</span>
            </div>
          )}
        </div>

        {/* Input Form */}
        <form onSubmit={handleSend} className="p-3 border-t border-gray-200 flex gap-2">
          <input
            type="text"
            placeholder="Type your policy question (e.g., Is ICU room capped? What is pre-hospitalization limit?)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-[#003178] hover:bg-blue-900 text-white px-5 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 shadow-xs"
          >
            <span>Send</span>
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

      {/* Feedback Reporting Ticket Form */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-4">
        <h4 className="font-bold text-gray-900 text-sm flex items-center gap-2">
          <Flag className="w-4 h-4 text-amber-600" />
          Report Incorrect Guidance / Submit Feedback Ticket
        </h4>
        <form onSubmit={handleTicketSubmit} className="space-y-3">
          <textarea
            rows="2"
            placeholder="Describe any discrepancy or clause error noticed in AI responses..."
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            className="w-full border border-gray-300 rounded-lg p-3 text-xs focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <div className="flex items-center justify-between flex-wrap gap-2">
            <button
              type="submit"
              className="bg-gray-800 hover:bg-gray-900 text-white px-4 py-2 rounded text-xs font-semibold"
            >
              Submit Feedback Ticket
            </button>
            {ticketCreated && (
              <span className="text-xs font-bold text-emerald-700 flex items-center gap-1">
                <Check className="w-4 h-4" />
                Ticket Created: #{ticketCreated} (SLA: 24 Hours)
              </span>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
