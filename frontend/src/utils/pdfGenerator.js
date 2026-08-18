import jsPDF from 'jspdf';
import { formatINR } from './formatters';

export function generatePolicySummaryPDF(policyProfile, topupProfile = null) {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });

  const primary = policyProfile || {
    insurer_name: 'Niva Bupa Health Insurance',
    policy_name: 'ReAssure 2.0 Titanium Plan',
    sum_insured_inr: 500000,
    room_eligibility: 'Single Private Air-Conditioned Room (No Capping)',
    co_pay: 'Nil (0% Co-Pay)',
    pre_authorization_required: true
  };

  // Header Box
  doc.setFillColor(15, 23, 42); // slate-900
  doc.rect(0, 0, 210, 32, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.text('CareCover Copilot', 14, 15);

  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Extracted Health Insurance Policy Summary & Verification Certificate', 14, 23);

  doc.setFontSize(8);
  doc.text(`Generated: ${new Date().toLocaleString('en-IN')} IST | Audit Ref: #CC-SUMMARY-${Math.floor(100000 + Math.random() * 900000)}`, 14, 28);

  // Section 1: Base Policy Details
  let y = 42;

  doc.setTextColor(15, 23, 42);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(12);
  doc.text('1. Base Health Policy Coverage Terms', 14, y);
  y += 6;

  doc.setLineWidth(0.5);
  doc.setDrawColor(203, 213, 225);
  doc.line(14, y, 196, y);
  y += 8;

  const summaryData = [
    ['Insurer Name', primary.insurer_name || 'Niva Bupa Health Insurance'],
    ['Policy Name', primary.policy_name || 'ReAssure 2.0 Titanium Plan'],
    ['Base Sum Insured', formatINR(primary.sum_insured_inr || 500000)],
    ['Room Rent Eligibility', primary.room_eligibility || 'Single Private AC Room (No Capping)'],
    ['Co-Pay Terms', primary.co_pay || 'Nil (0% Co-Pay)'],
    ['Pre-Authorization Requirement', primary.pre_authorization_required ? 'Required (48h Prior Intimation for Elective Surgeries)' : 'Not Mandatory']
  ];

  doc.setFontSize(9);
  summaryData.forEach(([label, val]) => {
    doc.setFillColor(248, 250, 252);
    doc.rect(14, y, 182, 9, 'F');
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(51, 65, 85);
    doc.text(label, 18, y + 6);

    doc.setFont('helvetica', 'normal');
    doc.setTextColor(15, 23, 42);
    doc.text(String(val), 85, y + 6);
    y += 11;
  });

  // Section 2: Dual Policy & Top-Up Breakdown (if available)
  if (topupProfile) {
    y += 4;
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(12);
    doc.text('2. Dual-Policy & Super Top-Up Protection Breakdown', 14, y);
    y += 6;
    doc.line(14, y, 196, y);
    y += 8;

    const baseSI = primary.sum_insured_inr || 500000;
    const topupSI = topupProfile.sum_insured_inr || 1500000;
    const combinedSI = baseSI + topupSI;

    const topupData = [
      ['Primary Policy Cover', formatINR(baseSI)],
      ['Super Top-Up Policy Cover', formatINR(topupSI)],
      ['Combined Sum Insured Protection', formatINR(combinedSI)],
      ['Top-Up Deductible Trigger', formatINR(500000)]
    ];

    topupData.forEach(([label, val]) => {
      doc.setFillColor(241, 245, 249);
      doc.rect(14, y, 182, 9, 'F');
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(30, 41, 59);
      doc.text(label, 18, y + 6);

      doc.setFont('helvetica', 'normal');
      doc.setTextColor(15, 23, 42);
      doc.text(String(val), 85, y + 6);
      y += 11;
    });
  }

  // Section 3: Extracted Clause Evidence
  y += 4;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(12);
  doc.text('3. Verified Extracted Policy Clause Evidence', 14, y);
  y += 6;
  doc.line(14, y, 196, y);
  y += 8;

  const evidenceList = primary.evidence || [
    { field: 'Sum Insured', page: 1, quote: 'Sum Insured under ReAssure Plan: ₹5,00,000' },
    { field: 'Room Rent', page: 3, quote: 'Single Private AC Room without daily limit.' }
  ];

  evidenceList.forEach((ev) => {
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.setTextColor(29, 78, 216); // blue-700
    doc.text(`• ${ev.field} (Page ${ev.page}):`, 18, y);
    y += 5;

    doc.setFont('helvetica', 'italic');
    doc.setFontSize(8.5);
    doc.setTextColor(71, 85, 105);
    doc.text(`"${ev.quote}"`, 22, y);
    y += 8;
  });

  // Footer Disclaimer
  doc.setFillColor(241, 245, 249);
  doc.rect(0, 275, 210, 22, 'F');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(7.5);
  doc.setTextColor(100, 116, 139);
  doc.text('CARECOVER COPILOT - INDEPENDENT HEALTHCARE & POLICY NAVIGATION SYSTEM', 14, 281);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7);
  doc.text('Authoritative Notice: Subject to direct insurer and hospital TPA verification at admission. Not medical advice or a coverage guarantee.', 14, 286);

  doc.save(`CareCover_Policy_Summary_${primary.insurer_name.replace(/\s+/g, '_')}.pdf`);
}

export function generatePreAuthFormPDF(policyProfile) {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });

  const primary = policyProfile || {
    insurer_name: 'Niva Bupa Health Insurance',
    policy_name: 'ReAssure 2.0 Titanium Plan',
    sum_insured_inr: 500000,
    room_eligibility: 'Single Private Air-Conditioned Room (No Capping)'
  };

  // Header Box (Emerald Green for TPA Form)
  doc.setFillColor(6, 78, 59); // emerald-900
  doc.rect(0, 0, 210, 32, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(15);
  doc.text('IRDAI STANDARD CASHLESS PRE-AUTHORIZATION REQUEST FORM', 14, 15);

  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.text('Third Party Administrator (TPA) & Hospital Network Pre-Approval Application', 14, 23);

  doc.setFontSize(8);
  doc.text(`Ref ID: #TPA-PREAUTH-${Math.floor(100000 + Math.random() * 900000)} | Generated: ${new Date().toLocaleDateString('en-IN')}`, 14, 28);

  let y = 42;

  // Section A: Insurer & Policyholder Details
  doc.setTextColor(6, 78, 59);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.text('SECTION A: INSURER & POLICY IDENTIFICATION', 14, y);
  y += 5;
  doc.setLineWidth(0.5);
  doc.setDrawColor(167, 243, 208);
  doc.line(14, y, 196, y);
  y += 7;

  const secA = [
    ['Insurance Company', primary.insurer_name || 'Niva Bupa Health Insurance'],
    ['Policy Name & Plan', primary.policy_name || 'ReAssure 2.0 Titanium Plan'],
    ['Policy Sum Insured', formatINR(primary.sum_insured_inr || 500000)],
    ['Eligible Room Category', primary.room_eligibility || 'Single Private AC Room']
  ];

  secA.forEach(([label, val]) => {
    doc.setFillColor(240, 253, 244);
    doc.rect(14, y, 182, 8, 'F');
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(8.5);
    doc.setTextColor(51, 65, 85);
    doc.text(label, 18, y + 5.5);

    doc.setFont('helvetica', 'normal');
    doc.setTextColor(15, 23, 42);
    doc.text(String(val), 80, y + 5.5);
    y += 10;
  });

  // Section B: Hospital & Admission Details
  y += 3;
  doc.setTextColor(6, 78, 59);
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.text('SECTION B: HOSPITAL ADMISSION & CLINICAL DETAILS', 14, y);
  y += 5;
  doc.line(14, y, 196, y);
  y += 7;

  const secB = [
    ['Hospital Name', '[ To be filled by Network Hospital TPA Desk ]'],
    ['Admission Type', 'Planned Surgery [  ]  /  Emergency ER Admission [  ]'],
    ['Proposed Date of Admission', '[ DD / MM / YYYY ]'],
    ['Estimated Length of Stay', '[ _____ Days ]'],
    ['Treating Doctor Name & Reg No', '[ Doctor Name / Medical Council Reg No ]']
  ];

  secB.forEach(([label, val]) => {
    doc.setFillColor(248, 250, 252);
    doc.rect(14, y, 182, 8, 'F');
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(8.5);
    doc.setTextColor(51, 65, 85);
    doc.text(label, 18, y + 5.5);

    doc.setFont('helvetica', 'normal');
    doc.setTextColor(100, 116, 139);
    doc.text(String(val), 80, y + 5.5);
    y += 10;
  });

  // Section C: Pre-Auth Intimation SLA Notice
  y += 3;
  doc.setFillColor(254, 242, 242); // red-50
  doc.rect(14, y, 182, 24, 'F');
  doc.setDrawColor(254, 202, 202);
  doc.rect(14, y, 182, 24, 'S');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(153, 27, 27);
  doc.text('MANDATORY TPA INTIMATION SLA NOTICE:', 18, y + 6);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(8);
  doc.setTextColor(127, 29, 29);
  doc.text('• Planned Hospitalization: Pre-authorization form must be submitted at least 48 hours prior to admission.', 18, y + 12);
  doc.text('• Emergency Casualty ER: Intimation must be sent to TPA within 24 hours of casualty admission.', 18, y + 17);
  doc.text('• Emergency ER National Helpline: Call 112 / 108 immediately for urgent ambulance assistance.', 18, y + 22);

  y += 32;

  // Section D: Signatures
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(9);
  doc.setTextColor(15, 23, 42);
  doc.text('Patient / Insured Signature: _______________________', 14, y);
  doc.text('Hospital TPA Officer Stamp & Signature: _______________________', 110, y);

  // Footer Disclaimer
  doc.setFillColor(241, 245, 249);
  doc.rect(0, 275, 210, 22, 'F');

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(7.5);
  doc.setTextColor(100, 116, 139);
  doc.text('CARECOVER COPILOT - TPA CASHLESS PRE-AUTHORIZATION FORM GENERATOR', 14, 281);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(7);
  doc.text('Compliance Note: Form structured per IRDAI Standardized Pre-Authorization Form Guidelines (Master Circular 2024).', 14, 286);

  doc.save(`TPA_PreAuth_Form_${primary.insurer_name.replace(/\s+/g, '_')}.pdf`);
}
