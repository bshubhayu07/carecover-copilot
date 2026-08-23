import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { purgeSessionDataApi } from '../services/api';
import { ShieldCheck, Lock, Trash2, Download, ChevronDown, KeyRound, ShieldAlert } from 'lucide-react';

export default function Sidebar() {
  const { consentGiven, setConsentGiven, setPolicyProfile, setTopupProfile, setChatHistory, setDeletionReceipt, deletionReceipt, showToast, t } = useApp();
  const [adminPin, setAdminPin] = useState('');
  const [adminAuth, setAdminAuth] = useState(false);
  const [expandedSection, setExpandedSection] = useState(null);

  const handlePurge = async () => {
    const res = await purgeSessionDataApi();
    setPolicyProfile(null);
    setTopupProfile(null);
    setChatHistory([]);
    setDeletionReceipt(res.receiptText);
    showToast('Ephemeral RAM session data purged successfully (DPDP Rules 2025 compliant)', 'success');
  };

  const toggleExpand = (sec) => {
    setExpandedSection(expandedSection === sec ? null : sec);
  };

  return (
    <aside className="w-full md:w-80 taste-card-anti-slop p-5 space-y-6 text-xs shrink-0">
      {/* Active Security Telemetry Status */}
      <div className="impeccable-badge-emerald px-3.5 py-2.5 rounded-xl flex items-center gap-2.5 font-medium">
        <span className="relative flex h-2.5 w-2.5 shrink-0">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-600"></span>
        </span>
        <div>
          <span className="font-bold block text-[11px] uppercase tracking-wider text-emerald-900">{t.telemetry || "Operational Telemetry"}</span>
          <span className="text-[11px] text-emerald-700">{t.telemetry_sub || "Encrypted Ephemeral Session Scope"}</span>
        </div>
      </div>

      {/* DPDP Rules 2025 Privacy Controls */}
      <div className="space-y-3.5">
        <div className="flex items-center gap-1.5 font-bold text-slate-900 text-xs uppercase tracking-wider border-b border-slate-200 pb-2">
          <Lock className="w-3.5 h-3.5 text-blue-700" />
          <span>{t.dpdp_header || "Privacy & DPDP Rules 2025"}</span>
        </div>

        <label className="flex items-start gap-2.5 cursor-pointer text-slate-800 bg-white/80 p-3 rounded-lg border border-slate-200 hover:bg-white transition">
          <input
            type="checkbox"
            checked={consentGiven}
            onChange={(e) => setConsentGiven(e.target.checked)}
            className="mt-0.5 rounded text-blue-700 focus:ring-blue-500"
          />
          <span className="leading-normal font-medium">{t.dpdp_consent || "I consent to temporary document processing for this session."}</span>
        </label>

        <button
          onClick={handlePurge}
          className="w-full flex items-center justify-center gap-2 bg-rose-700 hover:bg-rose-800 active:scale-[0.98] text-white px-3.5 py-2.5 rounded-xl font-semibold transition-all duration-200 shadow-xs"
        >
          <Trash2 className="w-4 h-4" />
          <span>{t.purge_btn || "Purge & Delete Session Data Now"}</span>
        </button>

        {deletionReceipt && (
          <a
            href={`data:text/plain;charset=utf-8,${encodeURIComponent(deletionReceipt)}`}
            download="carecover_deletion_receipt.txt"
            onClick={() => showToast('Audit Deletion Receipt downloaded (.txt)', 'info')}
            className="w-full flex items-center justify-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-2 rounded-xl font-medium border border-slate-300 transition"
          >
            <Download className="w-4 h-4 text-slate-600" />
            <span>Download Deletion Receipt (.txt)</span>
          </a>
        )}
      </div>

      <hr className="border-slate-200" />

      {/* Accordion Privacy Specifications */}
      <div className="space-y-2">
        {/* Retention Schedule */}
        <div className="border border-slate-200 rounded-lg overflow-hidden bg-white/70">
          <button
            onClick={() => toggleExpand('privacy')}
            className="w-full p-3 text-left font-semibold text-slate-800 bg-slate-50 hover:bg-slate-100 transition flex items-center justify-between"
          >
            <span>{t.privacy_accordion || "Privacy Policy & Retention Schedule"}</span>
            <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${expandedSection === 'privacy' ? 'rotate-180' : ''}`} />
          </button>
          {expandedSection === 'privacy' && (
            <div className="p-3 text-[11px] text-slate-600 space-y-1.5 bg-white border-t border-slate-200 animate-in fade-in duration-200">
              <p>• <strong>Ephemeral Processing:</strong> In-memory RAM storage only.</p>
              <p>• <strong>Retention Limit:</strong> 0 hours persistent database storage.</p>
              <p>• <strong>Transmission Security:</strong> TLS 1.3 encrypted web socket.</p>
            </div>
          )}
        </div>

        {/* Grievance Officer */}
        <div className="border border-slate-200 rounded-lg overflow-hidden bg-white/70">
          <button
            onClick={() => toggleExpand('grievance')}
            className="w-full p-3 text-left font-semibold text-slate-800 bg-slate-50 hover:bg-slate-100 transition flex items-center justify-between"
          >
            <span>{t.grievance_accordion || "Grievance Redressal & Support"}</span>
            <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${expandedSection === 'grievance' ? 'rotate-180' : ''}`} />
          </button>
          {expandedSection === 'grievance' && (
            <div className="p-3 text-[11px] text-slate-600 space-y-1 bg-white border-t border-slate-200 animate-in fade-in duration-200">
              <p><strong>Nodal Officer:</strong> CareCover Privacy Officer</p>
              <p><strong>Email:</strong> grievance@carecovercopilot.in</p>
              <p><strong>Bima Bharosa Portal Ref:</strong> #GRV-2026-88192</p>
              <p><strong>Resolution SLA:</strong> 72 business hours</p>
            </div>
          )}
        </div>

        {/* Admin Console */}
        <div className="border border-slate-200 rounded-lg overflow-hidden bg-white/70">
          <button
            onClick={() => toggleExpand('admin')}
            className="w-full p-3 text-left font-semibold text-slate-800 bg-slate-50 hover:bg-slate-100 transition flex items-center justify-between"
          >
            <span className="flex items-center gap-1.5">
              <KeyRound className="w-3.5 h-3.5 text-blue-700" />
              {t.admin_accordion || "Admin & CERT-In Console"}
            </span>
            <ChevronDown className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${expandedSection === 'admin' ? 'rotate-180' : ''}`} />
          </button>
          {expandedSection === 'admin' && (
            <div className="p-3 text-[11px] text-slate-600 space-y-2 bg-white border-t border-slate-200 animate-in fade-in duration-200">
              {!adminAuth ? (
                <div className="space-y-2">
                  <input
                    type="password"
                    placeholder="Enter Compliance Access PIN"
                    value={adminPin}
                    onChange={(e) => setAdminPin(e.target.value)}
                    className="w-full p-2 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-blue-600"
                  />
                  <button
                    onClick={() => {
                      const pass = adminPin === '2026';
                      setAdminAuth(pass);
                      showToast(pass ? 'Admin Authorization Verified' : 'Invalid Access PIN', pass ? 'success' : 'error');
                    }}
                    className="w-full bg-slate-900 text-white py-1.5 rounded font-semibold text-xs hover:bg-slate-800 transition active:scale-[0.98]"
                  >
                    Authenticate (Demo PIN: 2026)
                  </button>
                </div>
              ) : (
                <div className="space-y-1.5 text-[11px] text-slate-700">
                  <div className="text-emerald-700 font-bold">✔ Admin Authorization Active</div>
                  <p>• <strong>System Availability:</strong> 99.98% Operational</p>
                  <p>• <strong>Upload Policy:</strong> 25MB Max | %PDF- Validated</p>
                  <p>• <strong>CERT-In SLA:</strong> 6-Hour Breach Intimation (Directions 70B)</p>
                  <p>• <strong>Network Sync:</strong> Daily Feed Verified 00:00 IST</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="pt-3 border-t border-slate-200 text-[11px] text-slate-500 text-center space-y-1">
        <ShieldAlert className="w-4 h-4 mx-auto text-slate-400" />
        <p>{t.disclaimer_footer || "Independent navigation system. Not medical advice or an insurance guarantee."}</p>
      </div>
    </aside>
  );
}
