import React, { useState } from 'react';
import { useApp } from '../context/AppContext';
import { formatINR } from '../utils/formatters';
import { Calculator, CheckSquare, Shield, AlertTriangle } from 'lucide-react';

export default function CareJourneyTab() {
  const { t } = useApp();
  const [totalBill, setTotalBill] = useState(150000);
  const [copayPct, setCopayPct] = useState(10);
  const [nonMedical, setNonMedical] = useState(5000);
  const [allowedRoomRate, setAllowedRoomRate] = useState(5000);
  const [chosenRoomRate, setChosenRoomRate] = useState(10000);

  // Proportional Room Rent Penalty Logic
  const hasPenalty = chosenRoomRate > allowedRoomRate;
  const propRatio = hasPenalty ? allowedRoomRate / Number(chosenRoomRate) : 1.0;
  const propPenaltyPct = hasPenalty ? Math.round((1.0 - propRatio) * 1000) / 10 : 0;

  const associatedFees = (totalBill - nonMedical) * 0.70;
  const approvedAssocFees = associatedFees * propRatio;
  const propDeductionLoss = associatedFees - approvedAssocFees;

  const eligibleBase = totalBill - nonMedical - propDeductionLoss;
  const copayAmount = eligibleBase * (copayPct / 100.0);
  const estimatedCashless = Math.max(0, eligibleBase - copayAmount);
  const estimatedOutOfPocket = totalBill - estimatedCashless;

  return (
    <div className="space-y-6">
      {/* Tab Sub-navigation */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Calculator className="w-5 h-5 text-[#003178]" />
            Out-of-Pocket Claim & Proportional Penalty Estimator
          </h2>
          <p className="text-xs text-gray-500 mt-1">
            Estimate your personal cost sharing based on expected hospital bills, co-pay rules, and proportional room rent penalties.
          </p>
        </div>

        {/* Inputs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div>
            <label className="font-semibold text-gray-700 block mb-1">Estimated Hospital Bill (INR)</label>
            <input
              type="number"
              value={totalBill}
              onChange={(e) => setTotalBill(Number(e.target.value))}
              className="w-full border border-gray-300 rounded p-2 focus:outline-none"
            />
          </div>

          <div>
            <label className="font-semibold text-gray-700 block mb-1">Co-Pay Percentage (%)</label>
            <input
              type="number"
              value={copayPct}
              onChange={(e) => setCopayPct(Number(e.target.value))}
              className="w-full border border-gray-300 rounded p-2 focus:outline-none"
            />
          </div>

          <div>
            <label className="font-semibold text-gray-700 block mb-1">Non-Medical Consumables (INR)</label>
            <input
              type="number"
              value={nonMedical}
              onChange={(e) => setNonMedical(Number(e.target.value))}
              className="w-full border border-gray-300 rounded p-2 focus:outline-none"
            />
          </div>
        </div>

        {/* Proportional Room Rent Penalty Simulator Section */}
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 space-y-3 text-xs">
          <h3 className="font-bold text-gray-900 flex items-center gap-2 text-sm">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            Proportional Room Rent Penalty Simulator
          </h3>
          <p className="text-gray-600">
            If you choose a higher room rate than your policy limit, associated doctor fees and surgery charges are deducted proportionally.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="font-semibold text-gray-700 block mb-1">Policy Room Rent Limit / Day (INR)</label>
              <input
                type="number"
                value={allowedRoomRate}
                onChange={(e) => setAllowedRoomRate(Number(e.target.value))}
                className="w-full border border-gray-300 rounded p-2 focus:outline-none bg-white"
              />
            </div>

            <div>
              <label className="font-semibold text-gray-700 block mb-1">Chosen Hospital Room Rate / Day (INR)</label>
              <input
                type="number"
                value={chosenRoomRate}
                onChange={(e) => setChosenRoomRate(Number(e.target.value))}
                className="w-full border border-gray-300 rounded p-2 focus:outline-none bg-white"
              />
            </div>
          </div>

          {hasPenalty ? (
            <div className="bg-red-50 text-red-800 p-3 rounded border border-red-200 font-medium">
              ⚠ Proportional Payment Warning: Chosen room exceeds limit by {formatINR(chosenRoomRate - allowedRoomRate)}/day. Associated medical fees will face a <strong>{propPenaltyPct}% proportional deduction penalty!</strong>
            </div>
          ) : (
            <div className="bg-emerald-50 text-emerald-800 p-2.5 rounded border border-emerald-200 font-medium">
              ✔ No Proportional Room Penalty: Chosen room rate is within policy limit.
            </div>
          )}
        </div>

        {/* Output Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
            <span className="text-xs font-semibold text-emerald-800 uppercase block">Estimated Approved Cashless</span>
            <span className="text-2xl font-bold text-emerald-900 mt-1 block">{formatINR(estimatedCashless)}</span>
          </div>

          <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg text-center">
            <span className="text-xs font-semibold text-amber-800 uppercase block">Proportional Penalty Loss</span>
            <span className="text-2xl font-bold text-amber-900 mt-1 block">{formatINR(propDeductionLoss)}</span>
          </div>

          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-center">
            <span className="text-xs font-semibold text-red-800 uppercase block">Estimated Out-of-Pocket Cost</span>
            <span className="text-2xl font-bold text-red-900 mt-1 block">{formatINR(estimatedOutOfPocket)}</span>
          </div>
        </div>
      </div>

      {/* Patient Admission Checklist */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-4">
        <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
          <CheckSquare className="w-5 h-5 text-emerald-700" />
          Interactive Patient Checklist
        </h3>

        <div className="space-y-3 text-xs">
          <label className="flex items-center gap-2 p-2 bg-gray-50 rounded border border-gray-200 cursor-pointer">
            <input type="checkbox" defaultChecked className="rounded text-emerald-600" />
            <span>Pre-Authorization Request Form (Part A & B) submitted 48h prior</span>
          </label>
          <label className="flex items-center gap-2 p-2 bg-gray-50 rounded border border-gray-200 cursor-pointer">
            <input type="checkbox" defaultChecked className="rounded text-emerald-600" />
            <span>Doctor Admission Recommendation & Diagnostic Reports attached</span>
          </label>
          <label className="flex items-center gap-2 p-2 bg-gray-50 rounded border border-gray-200 cursor-pointer">
            <input type="checkbox" className="rounded text-emerald-600" />
            <span>Patient KYC Document (Aadhaar / PAN) verified at TPA Desk</span>
          </label>
        </div>
      </div>
    </div>
  );
}
