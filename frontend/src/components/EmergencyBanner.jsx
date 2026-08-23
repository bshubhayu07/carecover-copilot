import React from 'react';
import { useApp } from '../context/AppContext';
import { AlertOctagon, Phone } from 'lucide-react';

export default function EmergencyBanner() {
  const { t } = useApp();

  return (
    <div className="bg-rose-950 border-b border-rose-900/80 text-rose-100 px-4 py-2.5 shadow-xs">
      <div className="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-3 text-xs font-medium">
        <div className="flex items-center gap-2.5">
          <AlertOctagon className="w-4 h-4 text-rose-400 shrink-0" />
          <span className="text-slate-200">{t.emergency}</span>
        </div>
        <div className="flex items-center gap-2 bg-rose-900/80 text-rose-200 px-3 py-1 rounded font-semibold text-xs border border-rose-700/50 whitespace-nowrap">
          <Phone className="w-3.5 h-3.5 text-rose-400" />
          <span>Emergency ER: 112 / 108</span>
        </div>
      </div>
    </div>
  );
}
