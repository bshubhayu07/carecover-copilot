import React from 'react';
import type { PolicyClauses } from '../types/policy';

interface PolicySummaryCardProps {
  policy: PolicyClauses | null;
  t: (key: string) => string;
}

export const PolicySummaryCard: React.FC<PolicySummaryCardProps> = ({ policy, t }) => {
  if (!policy) {
    return (
      <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 text-slate-400 text-xs">
        No active policy loaded yet. Upload your policy PDF or select Demo Policy above.
      </div>
    );
  }

  return (
    <div className="bg-slate-900/90 p-6 rounded-xl border border-slate-700 space-y-4 shadow-xl">
      <div className="flex justify-between items-center border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-bold text-white">{policy.insurer_name}</h3>
          <p className="text-xs text-slate-400">{t('summary_sub')}</p>
        </div>
        <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded-full font-semibold">
          Policy Active
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block mb-1">{t('si_label')}</span>
          <strong className="text-sky-400 font-bold text-sm">₹{policy.sum_insured_inr.toLocaleString('en-IN')}</strong>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block mb-1">{t('room_label')}</span>
          <strong className="text-slate-100 font-bold text-sm">{policy.room_eligibility}</strong>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block mb-1">{t('copay_label')}</span>
          <strong className="text-emerald-400 font-bold text-sm">{policy.co_payment_percentage}% Co-Pay</strong>
        </div>
        <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block mb-1">Pre-Authorization</span>
          <strong className="text-amber-400 font-bold text-sm">{policy.pre_authorization_required ? "Required" : "Not Required"}</strong>
        </div>
      </div>
    </div>
  );
};
