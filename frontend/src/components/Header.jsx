import React from 'react';
import { useApp } from '../context/AppContext';
import { INDIAN_22_LANGUAGES } from '../utils/formatters';
import { ShieldCheck, Globe, FileText, MessageSquare, Building2, Activity } from 'lucide-react';

export default function Header() {
  const { language, setLanguage, activeTab, setActiveTab, t } = useApp();

  const tabs = [
    { id: 'tab1', label: t.tab1 || 'Upload & Extract', icon: FileText },
    { id: 'tab2', label: t.tab2 || 'Ask Your Policy', icon: MessageSquare },
    { id: 'tab3', label: t.tab3 || 'Find Hospital Options', icon: Building2 },
    { id: 'tab4', label: t.tab4 || 'Care Journey & Safety', icon: Activity },
  ];

  return (
    <header className="bg-slate-950/90 border-b border-slate-800 text-white sticky top-0 z-50 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 text-white p-2 rounded-lg shadow-sm">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-extrabold tracking-tight text-slate-100 font-display">CareCover Copilot</h1>
              <span className="bg-slate-800 text-blue-400 text-[10px] font-bold px-2 py-0.5 rounded border border-blue-500/20 uppercase tracking-widest">
                Enterprise
              </span>
            </div>
            <p className="text-xs text-slate-400 font-normal">
              Independent Clinical & Policy Decision Navigation Engine
            </p>
          </div>
        </div>

        {/* 22 Language Selection */}
        <div className="flex items-center gap-2 bg-slate-900 px-3.5 py-2 rounded-lg border border-slate-700/60 shadow-inner">
          <Globe className="w-4 h-4 text-blue-400" />
          <span className="text-xs text-slate-400 font-medium">Site Language:</span>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-transparent text-xs text-slate-100 font-semibold focus:outline-none cursor-pointer pr-1"
          >
            {INDIAN_22_LANGUAGES.map((lang) => (
              <option key={lang} value={lang} className="bg-slate-900 text-slate-100">
                {lang}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Tab Navigation */}
      <div className="bg-slate-900/90 border-t border-slate-800/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 flex gap-2 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-5 py-3 text-xs font-semibold transition-all border-b-2 whitespace-nowrap ${
                  isActive
                    ? 'border-blue-500 text-blue-400 bg-slate-800/80'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-blue-400' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
