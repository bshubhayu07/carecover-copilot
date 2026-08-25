import React, { useState } from 'react';
import { useI18n } from './hooks/useI18n';
import { Header } from './components/Header';
import { PolicySummaryCard } from './components/PolicySummaryCard';
import { ChatAssistant } from './components/ChatAssistant';
import type { PolicyClauses } from './types/policy';
import { extractPolicyPDF, purgeSessionData } from './services/api';

export function App() {
  const { language, setLanguage, t } = useI18n();
  const [activeTab, setActiveTab] = useState<'tab1' | 'tab2' | 'tab3' | 'tab4'>('tab1');
  const [isLightMode, setIsLightMode] = useState<boolean>(false);
  const [policy, setPolicy] = useState<PolicyClauses | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  const toggleTheme = () => {
    setIsLightMode(prev => !prev);
    document.documentElement.classList.toggle('light');
    document.documentElement.classList.toggle('dark');
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setUploadStatus(`Extracting clauses from '${file.name}'...`);

    try {
      const extracted = await extractPolicyPDF(file);
      setPolicy(extracted);
      setUploadStatus(`Extracted '${file.name}' successfully!`);
    } catch (err) {
      setUploadStatus("Extraction failed. Please load demo policy.");
    }
  };

  const handlePurge = async () => {
    try {
      await purgeSessionData();
      setPolicy(null);
      alert("Session memory purged successfully!");
    } catch (err) {
      alert("Failed to purge session.");
    }
  };

  return (
    <div className={`min-h-screen flex flex-col ${isLightMode ? 'bg-[#f7f4ee] text-[#1c1917]' : 'bg-[#080d1a] text-slate-100'}`}>
      <Header 
        selectedLanguage={language}
        onLanguageChange={setLanguage}
        isLightMode={isLightMode}
        onToggleTheme={toggleTheme}
        onPurgeData={handlePurge}
        t={t}
      />

      <main className="max-w-7xl mx-auto px-4 py-6 flex-1 w-full space-y-6">
        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 gap-6 text-sm font-semibold">
          <button 
            onClick={() => setActiveTab('tab1')}
            className={`pb-3 transition-all ${activeTab === 'tab1' ? 'border-b-2 border-sky-400 text-sky-400 font-bold' : 'text-slate-400'}`}
          >
            {t('tab1')}
          </button>
          <button 
            onClick={() => setActiveTab('tab2')}
            className={`pb-3 transition-all ${activeTab === 'tab2' ? 'border-b-2 border-sky-400 text-sky-400 font-bold' : 'text-slate-400'}`}
          >
            {t('tab2')}
          </button>
        </div>

        {/* Tab 1: Upload & Summary */}
        {activeTab === 'tab1' && (
          <div className="space-y-6">
            <div className="bg-slate-900/90 p-6 rounded-xl border border-slate-800 space-y-4">
              <h2 className="text-base font-bold text-white">{t('upload_title')}</h2>
              <p className="text-xs text-slate-400">{t('upload_desc')}</p>
              
              <input 
                type="file" 
                accept="application/pdf"
                onChange={handleFileUpload}
                className="block w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-sky-600 file:text-white hover:file:bg-sky-500 cursor-pointer"
              />
              {uploadStatus && <p className="text-xs text-emerald-400 font-semibold">{uploadStatus}</p>}
            </div>

            <PolicySummaryCard policy={policy} t={t} />
          </div>
        )}

        {/* Tab 2: Policy Q&A */}
        {activeTab === 'tab2' && (
          <ChatAssistant language={language} t={t} />
        )}
      </main>
    </div>
  );
}

export default App;
