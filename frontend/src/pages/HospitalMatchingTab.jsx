import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { getHospitalsApi } from '../services/api';
import { Hospital, MapPin, Search, ShieldCheck, AlertCircle, Radio } from 'lucide-react';

export default function HospitalMatchingTab() {
  const { currentCity, setCurrentCity, useLocation, setUseLocation, t } = useApp();
  const [city, setCity] = useState('Pune');
  const [specialty, setSpecialty] = useState('All Specialties');
  const [inNetworkOnly, setInNetworkOnly] = useState(false);
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);

  const cities = ['Pune', 'Mumbai', 'Delhi', 'Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata'];

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const res = await getHospitalsApi(city, specialty, inNetworkOnly);
      setHospitals(res);
      setLoading(false);
    }
    loadData();
  }, [city, specialty, inNetworkOnly]);

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm space-y-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Hospital className="w-5 h-5 text-[#003178]" />
            {t.hosp_header}
          </h2>
          <p className="text-xs text-gray-500 mt-1">
            Data Source Citation: Sourced directly from published insurer directories (Niva Bupa, Star Health, ICICI Lombard). Authoritative Notice: Subject to insurer confirmation at admission.
          </p>
        </div>

        {/* Location Controls */}
        <div className="flex flex-wrap items-center justify-between gap-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
          <div className="flex items-center gap-2">
            <label className="flex items-center gap-2 text-xs font-semibold text-gray-700 cursor-pointer">
              <input
                type="checkbox"
                checked={useLocation}
                onChange={(e) => setUseLocation(e.target.checked)}
                className="rounded text-blue-800 focus:ring-blue-500"
              />
              <span>Allow Access to My Current Physical Location</span>
            </label>
          </div>

          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-red-600 shrink-0" />
            <select
              value={city}
              onChange={(e) => {
                setCity(e.target.value);
                setCurrentCity(e.target.value);
              }}
              className="bg-white border border-gray-300 text-xs font-semibold rounded px-3 py-1.5 focus:outline-none"
            >
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-semibold text-gray-600 block mb-1">Filter Specialty</label>
            <select
              value={specialty}
              onChange={(e) => setSpecialty(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 text-xs focus:outline-none"
            >
              <option value="All Specialties">All Specialties</option>
              <option value="Cardiology">Cardiology</option>
              <option value="Oncology">Oncology</option>
              <option value="Orthopedics">Orthopedics</option>
              <option value="Neurology">Neurology</option>
            </select>
          </div>

          <div className="flex items-end">
            <label className="flex items-center gap-2 text-xs font-semibold text-gray-700 cursor-pointer pb-2">
              <input
                type="checkbox"
                checked={inNetworkOnly}
                onChange={(e) => setInNetworkOnly(e.target.checked)}
                className="rounded text-emerald-600 focus:ring-emerald-500"
              />
              <span>Show In-Network Cashless Only</span>
            </label>
          </div>
        </div>
      </div>

      {/* Hospital List Cards */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-gray-700 uppercase tracking-wider">
          Found {hospitals.length} Cashless Network Hospitals in {city}
        </h3>

        {loading ? (
          <div className="p-8 text-center text-sm text-gray-500 bg-white rounded border border-gray-200">
            Fetching cashless provider directory...
          </div>
        ) : (
          hospitals.map((hosp) => (
            <div key={hosp.id} className="bg-white p-5 rounded-lg border border-gray-200 shadow-xs hover:border-blue-300 transition space-y-3">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h4 className="text-base font-bold text-gray-900 flex items-center gap-2">
                    {hosp.name}
                    <span className="bg-emerald-100 text-emerald-800 text-[11px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                      {hosp.network_status}
                    </span>
                  </h4>
                  <p className="text-xs text-gray-600 mt-1">Specialties: {hosp.specialties}</p>
                </div>

                <div className="text-right">
                  <span className="text-xs text-gray-500 block">Match Score</span>
                  <span className="text-lg font-bold text-blue-900">{hosp.score} pts</span>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-gray-50 p-3 rounded border border-gray-100">
                <div>
                  <span className="font-semibold text-gray-500 block">Eligible Room Rent</span>
                  <span className="font-medium text-gray-800">{hosp.eligible_room}</span>
                </div>
                <div>
                  <span className="font-semibold text-gray-500 block">GPS Distance</span>
                  <span className="font-medium text-gray-800">{hosp.distance} km from {currentCity}</span>
                </div>
              </div>

              <div className="bg-blue-50/60 text-blue-900 p-3 rounded text-xs">
                <strong>Matching Rule:</strong> {hosp.explanation}
              </div>

              {hosp.caveat && (
                <div className="bg-amber-50 text-amber-800 p-2.5 rounded text-xs flex items-center gap-1.5 border border-amber-200/60">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
                  <span>{hosp.caveat}</span>
                </div>
              )}

              <div className="text-[10px] text-gray-400 border-t border-gray-100 pt-2 flex items-center justify-between">
                <span>Record Feed ID: {hosp.feed_id || 'FEED-NIVABUPA-20260816-01'}</span>
                <span>Refresh Schedule: Daily Auto-Sync 00:00 IST</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
