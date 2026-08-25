import React, { useState } from 'react';
import type { ChatMessage } from '../types/chat';
import { askPolicyQuestion } from '../services/api';

interface ChatAssistantProps {
  language: string;
  t: (key: string) => string;
}

export const ChatAssistant: React.FC<ChatAssistantProps> = ({ language, t }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: t('chat_intro'),
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [inputQuery, setInputQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleSend = async () => {
    if (!inputQuery.trim() || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputQuery,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMsg]);
    const query = inputQuery;
    setInputQuery('');
    setLoading(true);

    try {
      const res = await askPolicyQuestion(query, language);
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: res.answer,
        timestamp: new Date().toLocaleTimeString(),
        sources: res.policy_clauses_used
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "Sorry, I ran into an error querying policy data. Please try again.",
        timestamp: new Date().toLocaleTimeString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900/90 rounded-xl border border-slate-800 flex flex-col h-[550px] shadow-2xl overflow-hidden">
      <div className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-950/60">
        <h3 className="font-bold text-white text-sm">{t('ask_title')}</h3>
        <span className="text-xs text-emerald-400 font-medium">Groq RAG Active</span>
      </div>

      <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs">
        {messages.map(msg => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-3.5 space-y-1 ${
              msg.role === 'user' 
                ? 'bg-sky-600 text-white rounded-br-none' 
                : msg.isError 
                ? 'bg-red-950/80 text-red-300 border border-red-800' 
                : 'bg-slate-800 text-slate-100 border border-slate-700 rounded-bl-none'
            }`}>
              <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <span className="text-[10px] text-slate-400 block text-right">{msg.timestamp}</span>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-sky-400 p-3 rounded-2xl rounded-bl-none border border-slate-700 text-xs animate-pulse">
              Consulting RAG policy embeddings...
            </div>
          </div>
        )}
      </div>

      <div className="p-3 border-t border-slate-800 bg-slate-950/60 flex gap-2">
        <input 
          type="text"
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder={t('chat_placeholder')}
          className="flex-1 bg-slate-900 border border-slate-700 text-white text-xs rounded-lg px-3 py-2"
        />
        <button 
          onClick={handleSend}
          disabled={loading}
          className="bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-4 py-2 rounded-lg cursor-pointer transition-all"
        >
          {t('send_btn')}
        </button>
      </div>
    </div>
  );
};
