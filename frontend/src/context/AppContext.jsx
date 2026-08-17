import React, { createContext, useContext, useState } from 'react';
import { getTranslation } from '../utils/formatters';
import SonnerToast from '../components/SonnerToast';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [activeTab, setActiveTab] = useState('tab1');
  const [language, setLanguage] = useState('English');
  const [policyProfile, setPolicyProfile] = useState(null);
  const [topupProfile, setTopupProfile] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [consentGiven, setConsentGiven] = useState(true);
  const [deletionReceipt, setDeletionReceipt] = useState(null);
  const [toast, setToast] = useState({ message: '', type: 'success' });

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
  };

  const clearToast = () => {
    setToast({ message: '', type: 'success' });
  };

  const t = getTranslation(language);

  return (
    <AppContext.Provider
      value={{
        activeTab,
        setActiveTab,
        language,
        setLanguage,
        policyProfile,
        setPolicyProfile,
        topupProfile,
        setTopupProfile,
        chatHistory,
        setChatHistory,
        consentGiven,
        setConsentGiven,
        deletionReceipt,
        setDeletionReceipt,
        t,
        showToast
      }}
    >
      {children}
      {toast.message && (
        <SonnerToast
          message={toast.message}
          type={toast.type}
          onClose={clearToast}
        />
      )}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
