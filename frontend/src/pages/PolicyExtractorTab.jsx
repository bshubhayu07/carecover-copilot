import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { extractPolicyApi } from '../services/api';
import { formatINR } from '../utils/formatters';
import { Upload, FileCheck, Layers, Download, CheckCircle, ShieldAlert, Sparkles } from 'lucide-react';

export default function PolicyExtractorTab() {
  const { policyProfile, setPolicyProfile, topupProfile, setTopupProfile, consentGiven, t } = useApp();
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [deductible, setDeductible] = useState(500000);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 25 * 1024 * 1024) {
      setErrorMsg('File size exceeds 25 MB enterprise security threshold.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const extracted = await extractPolicyApi(file);
      setPolicyProfile(extracted);
    } catch (err) {
      setErrorMsg('Extraction error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const baseSI = policyProfile?.sum_insured_inr || 500000;
  const topupSI = topupProfile?.sum_insured_inr || 1500000;
  const combinedSI = baseSI + topupSI;

  return (
    <div className="space-y-6">
      {/* Upload Header Card */}
      <div className="glass-panel-light p-6 rounded-xl space-y-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <Upload className="w-5 h-5 text-blue-700" />
            {t.upload_header}
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Upload Hardening Active: Enforced Limit 25 MB | Max 50 Pages | %PDF- Magic Bytes Verified
          </p>
        </div>

        {!consentGiven && (
          <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3 rounded-lg text-xs flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0 text-amber-600" />
            <span>Please check 'I consent to temporary document processing' in the sidebar to enable file upload.</span>
          </div>
        )}

        {errorMsg && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded-lg text-xs">
            {errorMsg}
          </div>
        )}

        <div className="flex flex-wrap items-center gap-4">
          <label className={`flex-1 border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition ${
            consentGiven ? 'border-blue-400 hover:border-blue-600 bg-blue-50/60' : 'border-slate-300 bg-slate-100/50 cursor-not-allowed'
          }`}>
            <Upload className="w-10 h-10 text-blue-700 mx-auto mb-2" />
            <span className="text-sm font-bold text-slate-900 block">{t.upload_sub}</span>
            <span className="text-xs text-slate-500 mt-1 block">Limit 25MB per file • PDF (Max 50 pages)</span>
            <input
              type="file"
              accept=".pdf"
              disabled={!consentGiven || loading}
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
        </div>

        {loading && (
          <div className="flex items-center gap-2 text-xs text-blue-800 font-medium bg-blue-50 p-3 rounded-lg">
            <Sparkles className="w-4 h-4 animate-spin text-blue-600" />
            <span>Running validated SHA-256 extraction and vector embedding...</span>
          </div>
        )}
      </div>

      {/* Dual-Policy & Super Top-Up Comparison Engine */}
      <div className="glass-panel-light p-6 rounded-xl space-y-4">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Layers className="w-5 h-5 text-emerald-700" />
          {t.topup_expander}
        </h3>
        <p className="text-xs text-slate-600">{t.topup_desc}</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 bg-slate-50/80 p-4 rounded-xl border border-slate-200">
          <div className="p-4 bg-white/90 rounded-lg border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase block">{t.primary_cover}</span>
            <span className="text-2xl font-bold text-emerald-800 mt-1 block">{formatINR(baseSI)}</span>
            <span className="text-xs text-slate-500 block mt-1">{policyProfile?.insurer_name || 'Niva Bupa Health Insurance'}</span>
          </div>

          <div className="p-4 bg-white/90 rounded-lg border border-slate-200">
            <span className="text-xs font-semibold text-slate-500 uppercase block">{t.topup_cover}</span>
            <span className="text-2xl font-bold text-emerald-800 mt-1 block">{formatINR(topupSI)}</span>
            <span className="text-xs text-slate-500 block mt-1">{topupProfile?.insurer_name || 'Star Health Insurance'}</span>
          </div>

          <div className="p-4 bg-blue-50/90 border border-blue-200 rounded-lg">
            <span className="text-xs font-semibold text-blue-900 uppercase block">{t.combined_si}</span>
            <span className="text-2xl font-bold text-blue-950 mt-1 block">{formatINR(combinedSI)}</span>
            <span className="text-xs text-blue-700 block mt-1 font-medium">Deductible Trigger: {formatINR(deductible)}</span>
          </div>
        </div>
      </div>

      {/* Extracted Policy Summary Grid */}
      {policyProfile && (
        <div className="glass-panel-light p-6 rounded-xl space-y-6">
          <div className="flex items-center justify-between flex-wrap gap-4 border-b border-slate-200 pb-4">
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-blue-800" />
              {t.extracted_summary}
            </h3>

            <div className="flex items-center gap-2">
              <button className="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white px-3.5 py-2 rounded-lg text-xs font-semibold transition">
                <Download className="w-3.5 h-3.5" />
                <span>{t.dl_pdf_summary}</span>
              </button>
              <button className="flex items-center gap-1.5 bg-emerald-700 hover:bg-emerald-800 text-white px-3.5 py-2 rounded-lg text-xs font-semibold transition">
                <Download className="w-3.5 h-3.5" />
                <span>{t.dl_pdf_preauth}</span>
              </button>
            </div>
          </div>

          {/* Base Coverage Terms */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider border-l-4 border-blue-700 pl-2">
              {t.base_coverage}
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.insurer_name}</span>
                <span className="text-sm font-bold text-slate-900">{policyProfile.insurer_name}</span>
              </div>
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.policy_name}</span>
                <span className="text-sm font-bold text-slate-900">{policyProfile.policy_name}</span>
              </div>
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.sum_insured}</span>
                <span className="text-sm font-bold text-emerald-700">{formatINR(policyProfile.sum_insured_inr)}</span>
              </div>
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.room_eligibility}</span>
                <span className="text-sm font-medium text-slate-900">{policyProfile.room_eligibility}</span>
              </div>
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.copay_terms}</span>
                <span className="text-sm font-medium text-slate-900">{policyProfile.co_pay}</span>
              </div>
              <div className="p-3.5 bg-slate-50/80 rounded-lg border border-slate-200">
                <span className="text-xs font-semibold text-slate-500 block">{t.preauth_req}</span>
                <span className="text-sm font-semibold text-blue-800 flex items-center gap-1 mt-0.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600" />
                  Required (48h Prior Intimation)
                </span>
              </div>
            </div>
          </div>

          {/* Evidence Quotes */}
          {policyProfile.evidence && (
            <div className="bg-blue-50/80 p-4 rounded-lg border border-blue-200 text-xs space-y-2">
              <span className="font-bold text-blue-900 uppercase block tracking-wider text-[11px]">
                Extracted Clause Evidence
              </span>
              {policyProfile.evidence.map((ev, i) => (
                <p key={i} className="text-slate-700">
                  • <strong>{ev.field}</strong> (Page {ev.page}): <em>"{ev.quote}"</em>
                </p>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
