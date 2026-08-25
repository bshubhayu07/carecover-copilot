import React from 'react';
import type { IndianLanguage } from '../types/i18n';

interface HeaderProps {
  selectedLanguage: IndianLanguage;
  onLanguageChange: (lang: IndianLanguage) => void;
  isLightMode: boolean;
  onToggleTheme: () => void;
  onPurgeData: () => void;
  t: (key: string) => string;
}

export const LANGUAGES: IndianLanguage[] = [
  "English", "Hindi", "Marathi", "Bengali", "Gujarati",
  "Punjabi", "Tamil", "Telugu", "Kannada", "Malayalam",
  "Odia", "Assamese", "Urdu", "Sanskrit", "Kashmiri",
  "Nepali", "Sindhi", "Konkani", "Maithili", "Dogri",
  "Manipuri", "Bodo", "Santhali"
];

export const Header: React.FC<HeaderProps> = ({
  selectedLanguage,
  onLanguageChange,
  isLightMode,
  onToggleTheme,
  onPurgeData,
  t
}) => {
  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-sky-500/10 p-2 rounded-xl border border-sky-500/20">
            <svg className="w-6 h-6 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <div>
            <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
              CareCover Copilot
              <span className="text-xs bg-sky-950 text-sky-400 border border-sky-800 px-2 py-0.5 rounded-full font-medium">v2.5 Enterprise</span>
            </h1>
            <p className="text-xs text-slate-400">{t('header_subtitle')}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <select 
            value={selectedLanguage}
            onChange={(e) => onLanguageChange(e.target.value as IndianLanguage)}
            className="bg-slate-900 border border-slate-700 text-white text-xs rounded-lg px-3 py-2"
          >
            {LANGUAGES.map(lang => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>

          <button 
            onClick={onToggleTheme}
            className="bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs px-3.5 py-2 rounded-lg shadow-md border border-sky-400 transition-all flex items-center gap-1.5 cursor-pointer"
          >
            {isLightMode ? "Switch to Dark Mode" : "Switch to Light Mode"}
          </button>

          <button 
            onClick={onPurgeData}
            className="bg-red-950/80 hover:bg-red-900/80 text-red-300 font-semibold text-xs px-3 py-2 rounded-lg border border-red-800 transition-all"
          >
            {t('purge_btn')}
          </button>
        </div>
      </div>
    </header>
  );
};
