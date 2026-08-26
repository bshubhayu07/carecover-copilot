from typing import Dict, Any

CITY_COST_MULTIPLIERS = {
    "Delhi": 1.20,
    "Mumbai": 1.25,
    "Bengaluru": 1.15,
    "Hyderabad": 1.10,
    "Chennai": 1.10,
    "Pune": 1.00,
    "Kolkata": 0.95,
    "Ahmedabad": 0.95,
    "Jaipur": 0.90,
    "Lucknow": 0.85,
    "Chandigarh": 0.95,
    "Kochi": 0.90,
    "Bhopal": 0.80,
    "Bhubaneswar": 0.80,
    "Patna": 0.80,
    "Guwahati": 0.80,
    "Visakhapatnam": 0.85,
    "Raipur": 0.80,
    "Ranchi": 0.80,
    "Dehradun": 0.85,
    "Shimla": 0.85,
    "Panaji": 0.95
}

BASE_PROCEDURE_BENCHMARKS = {
    "Cataract Surgery (Per Eye)": {"base": 45000, "icu_avg": 0, "stay_days": "Day Care (4 Hours)"},
    "Total Knee Replacement Surgery": {"base": 220000, "icu_avg": 25000, "stay_days": "4-5 Days"},
    "Total Hip Replacement Surgery": {"base": 240000, "icu_avg": 25000, "stay_days": "5-6 Days"},
    "Coronary Artery Bypass Graft (CABG)": {"base": 350000, "icu_avg": 60000, "stay_days": "7-9 Days"},
    "Cardiac Stent Angioplasty": {"base": 180000, "icu_avg": 30000, "stay_days": "2-3 Days"},
    "Chemotherapy Cycle & Targeted Therapy": {"base": 65000, "icu_avg": 0, "stay_days": "1 Day Care"},
    "Laparoscopic Cholecystectomy (Gallbladder)": {"base": 75000, "icu_avg": 12000, "stay_days": "2 Days"},
    "Kidney Stone Surgery (RIRS / PCNL)": {"base": 95000, "icu_avg": 15000, "stay_days": "2 Days"},
    "Maternity C-Section Delivery": {"base": 85000, "icu_avg": 10000, "stay_days": "3-4 Days"},
    "Brain Tumor Craniotomy Surgery": {"base": 550000, "icu_avg": 120000, "stay_days": "10-14 Days"}
}

def estimate_treatment_cost(procedure_name: str, city: str = "Pune") -> Dict[str, Any]:
    """
    Estimates procedure treatment costs, ICU charges, and expected insurance coverage % by city.
    Supports fuzzy matching and unknown procedure detection.
    """
    multiplier = CITY_COST_MULTIPLIERS.get(city, 1.0)
    
    # Fuzzy matching against benchmarks
    proc_clean = procedure_name.lower().strip()
    found_key = None
    for key in BASE_PROCEDURE_BENCHMARKS:
        k_clean = key.lower().strip()
        if k_clean == proc_clean or proc_clean in k_clean or k_clean in proc_clean:
            found_key = key
            break
            
    is_known = found_key is not None
    proc_info = BASE_PROCEDURE_BENCHMARKS.get(found_key or "", {"base": 120000, "icu_avg": 20000, "stay_days": "3 Days"})
    
    estimated_cost = round(proc_info["base"] * multiplier, 2)
    estimated_icu = round(proc_info["icu_avg"] * multiplier, 2)
    
    cost_range_min = round(estimated_cost * 0.85, 2)
    cost_range_max = round(estimated_cost * 1.20, 2)
    
    return {
        "procedure_name": found_key or procedure_name,
        "query_procedure": procedure_name,
        "procedure_found": is_known,
        "city": city,
        "city_multiplier": multiplier,
        "estimated_average_cost": estimated_cost,
        "cost_range_min": cost_range_min,
        "cost_range_max": cost_range_max,
        "estimated_icu_charge": estimated_icu,
        "typical_hospital_stay": proc_info["stay_days"],
        "projected_insurance_coverage_percent": 94.0 if is_known else 80.0,
        "cashless_pre_auth_required": True,
        "note": "Standard procedure benchmark loaded." if is_known else "Unrecognized procedure name; displaying generic baseline healthcare cost estimate."
    }

