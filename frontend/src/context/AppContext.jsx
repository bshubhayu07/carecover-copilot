import React, { createContext, useContext, useState } from 'react';
import { TRANSLATIONS } from '../utils/formatters';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [activeTab, setActiveTab] = useState('tab1');
  const [consentGiven, setConsentGiven] = useState(true);
  
  // Policy & Extraction Data
  const [policyProfile, setPolicyProfile] = useState({
    insurer_name: 'Niva Bupa Health Insurance',
    policy_name: 'ReAssure 2.0 Titanium Plan',
    sum_insured_inr: 500000,
    room_eligibility: 'Single Private Air-Conditioned Room (No Capping)',
    co_pay: 'Nil (0% Co-Pay)',
    pre_authorization_required: true,
    evidence: [
      { field: 'Sum Insured', page: 1, quote: 'Sum Insured under ReAssure Plan: ₹5,00,000' },
      { field: 'Room Rent', page: 3, quote: 'Single Private AC Room without daily cap.' }
    ]
  });

  const [topupProfile, setTopupProfile] = useState({
    insurer_name: 'Star Health Insurance',
    policy_name: 'Super Surplus Extra Plan',
    sum_insured_inr: 1500000,
    co_pay: 'Nil (0%)',
    deductible_inr: 500000
  });

  // Chat & Location State
  const [chatHistory, setChatHistory] = useState([
    {
      role: 'assistant',
      content: 'Hello! I am your CareCover Copilot. Ask me any question about your policy terms, room rent limits, pre-authorization, or claim procedures.',
      trace_id: 'RAG-TRACE-SYSTEM-INIT'
    }
  ]);
  const [currentCity, setCurrentCity] = useState('Pune');
  const [useLocation, setUseLocation] = useState(false);
  const [deletionReceipt, setDeletionReceipt] = useState(null);

  const t = TRANSLATIONS[selectedLanguage] || TRANSLATIONS['English'];

  return (
    <AppContext.Provider
      value={{
        selectedLanguage,
        setSelectedLanguage,
        activeTab,
        setActiveTab,
        consentGiven,
        setConsentGiven,
        policyProfile,
        setPolicyProfile,
        topupProfile,
        setTopupProfile,
        chatHistory,
        setChatHistory,
        currentCity,
        setCurrentCity,
        useLocation,
        setUseLocation,
        deletionReceipt,
        setDeletionReceipt,
        t
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
