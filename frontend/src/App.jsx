import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
import Header from './components/Header';
import EmergencyBanner from './components/EmergencyBanner';
import Sidebar from './components/Sidebar';
import PolicyExtractorTab from './pages/PolicyExtractorTab';
import PolicyAskTab from './pages/PolicyAskTab';
import HospitalMatchingTab from './pages/HospitalMatchingTab';
import CareJourneyTab from './pages/CareJourneyTab';

function MainContent() {
  const { activeTab } = useApp();

  return (
    <div className="flex-1 p-4 md:p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        {activeTab === 'tab1' && <PolicyExtractorTab />}
        {activeTab === 'tab2' && <PolicyAskTab />}
        {activeTab === 'tab3' && <HospitalMatchingTab />}
        {activeTab === 'tab4' && <CareJourneyTab />}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AppProvider>
      <div className="min-h-screen flex flex-col bg-app-ambient text-slate-900 font-sans">
        <Header />
        <EmergencyBanner />

        <div className="flex-1 flex flex-col md:flex-row max-w-7xl w-full mx-auto p-2 md:p-4 gap-4">
          <Sidebar />
          <MainContent />
        </div>
      </div>
    </AppProvider>
  );
}
