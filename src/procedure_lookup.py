from typing import Dict, Any

PROCEDURE_DATABASE: Dict[str, Dict[str, Any]] = {
    "Cataract Surgery (Per Eye)": {
        "estimated_cost": 45000,
        "sub_limit": "INR 40,000 per eye (max INR 80,000 total)",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Ophthalmologist Consultation Note", "A-Scan Biometry Report", "Lens Invoice Sticker"],
        "guidance": "Cataract is classified as a Day Care procedure. Ensure lens brand invoice is preserved for claim approval."
    },
    "LASIK / Refractive Eye Surgery": {
        "estimated_cost": 65000,
        "sub_limit": "Covered only if refractive error is >= +/- 7.5 Diopters",
        "waiting_period": "24 months waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Refraction Report", "Corneal Topography Scan", "Ophthalmologist Prescription"],
        "guidance": "Cosmetic LASIK is excluded. Medical necessity threshold requires refractive power >= 7.5D."
    },
    "Total Knee Replacement Surgery": {
        "estimated_cost": 250000,
        "sub_limit": "Capped at INR 2,50,000 per knee or room limit baseline",
        "waiting_period": "24 to 48 months pre-existing / specific disease clause",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["X-Ray Weight Bearing View Report", "Orthopedic Surgeon Recommendation", "Implant Serial Sticker"],
        "guidance": "Inpatient admission required (min 48 hours). Verify implant cost capping rules with TPA."
    },
    "Total Hip Replacement Surgery": {
        "estimated_cost": 280000,
        "sub_limit": "Capped at INR 2,80,000 per joint or room limit baseline",
        "waiting_period": "24 to 48 months pre-existing / specific disease clause",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Pelvis Hip X-Ray / MRI Report", "Orthopedic Surgeon Recommendation", "Implant Barcode Sticker"],
        "guidance": "Requires minimum 3-4 days inpatient hospitalization. Check room rent capping impact."
    },
    "ACL / Knee Ligament Arthroscopy": {
        "estimated_cost": 120000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial (immediate for accidental sports injury)",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Knee MRI Scan Report", "Arthroscopy OT Notes", "Graft / Bio-Screw Invoice"],
        "guidance": "Day care or 24-hour admission eligible. Accidental trauma waives initial waiting period."
    },
    "Spine Microdiscectomy / Disc Surgery": {
        "estimated_cost": 210000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Lumbar Spine MRI Report", "Neurosurgeon Referral", "Implant / Cage Invoice"],
        "guidance": "Inpatient hospitalization required. Pre-authorization required 48 hours prior."
    },
    "Coronary Artery Bypass Graft (CABG)": {
        "estimated_cost": 450000,
        "sub_limit": "Up to Base Sum Insured (ICU & Surgery Covered 100%)",
        "waiting_period": "30 days initial (36-48 months if pre-existing heart condition)",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Coronary Angiography (CAG) Report", "Cardiac Surgeon Referral", "ECHO / ECG Charts"],
        "guidance": "Major cardiac procedure. ICU stays are fully covered without room capping."
    },
    "Cardiac Stent Angioplasty": {
        "estimated_cost": 180000,
        "sub_limit": "Up to Base Sum Insured (Stent cost capped as per NPPA guidelines)",
        "waiting_period": "30 days initial, 36 months if pre-existing cardiac history",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Coronary Angiography (CAG) Report", "Cardiologist Referral", "Stent Barcode & Invoice"],
        "guidance": "Emergency pre-authorization permitted within 24 hours of hospital admission."
    },
    "Pacemaker Implantation Surgery": {
        "estimated_cost": 220000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial (36 months for pre-existing cardiac arrhythmia)",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Holter Monitor / ECG Report", "Cardiologist Recommendation", "Pacemaker Serial Sticker"],
        "guidance": "Inpatient admission required. Verify device serial sticker attached to final bill."
    },
    "Chemotherapy Cycle & Targeted Therapy": {
        "estimated_cost": 95000,
        "sub_limit": "Covered under Day Care Benefit up to Sum Insured",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Oncologist Biopsy / Histopathology Report", "Chemotherapy Cycle Protocol Sheet", "Drug Invoices"],
        "guidance": "Day care procedure. Does not require 24-hour stay. Target biological drugs covered."
    },
    "Radiation Therapy (IMRT / CyberKnife)": {
        "estimated_cost": 240000,
        "sub_limit": "Covered up to Base Sum Insured",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["PET-CT / MRI Scan Report", "Radiation Oncologist Plan", "Session Log Summary"],
        "guidance": "Modern robotic radiation therapies (CyberKnife/Proton) covered subject to policy modern treatment caps."
    },
    "Cancer Tumor Surgical Resection": {
        "estimated_cost": 380000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Biopsy Report", "Surgical Oncology OT Notes", "Histopathology Specimen Report"],
        "guidance": "Inpatient hospitalization required. Pre-authorization required 48h prior."
    },
    "Laparoscopic Cholecystectomy (Gallbladder)": {
        "estimated_cost": 85000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["USG Abdomen Report showing Gallstones", "Surgeon OT Notes", "Histopathology Report"],
        "guidance": "Laparoscopic procedure eligible under Day Care or 24-hour admission."
    },
    "Laparoscopic Appendectomy": {
        "estimated_cost": 75000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial (Immediate for acute appendicitis emergency)",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["USG / CT Abdomen Report", "Surgeon OT Notes", "Emergency Admission Intimation"],
        "guidance": "Acute appendicitis is an emergency admission. Pre-auth intimation within 24h."
    },
    "Hernia Mesh Repair Surgery": {
        "estimated_cost": 90000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["USG Clinical Examination Report", "Surgeon Recommendation", "Mesh Sticker Invoice"],
        "guidance": "Inguinal, umbilical, or incisional hernia subject to 24-month waiting period."
    },
    "General Major Surgery": {
        "estimated_cost": 150000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Diagnostic Test Reports", "Surgeon OT Notes", "Itemized Final Hospital Bill"],
        "guidance": "Inpatient admission required min 24 hours. Room rent capping applies."
    },
    "Kidney Stone Surgery (RIRS / PCNL)": {
        "estimated_cost": 95000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["NCCT KUB Scan Report", "Urologist OT Notes", "Stent Removal Summary"],
        "guidance": "Advanced laser RIRS / PCNL covered under day care or 24-hour stay."
    },
    "Hemodialysis Session": {
        "estimated_cost": 15000,
        "sub_limit": "Covered under Day Care Benefit",
        "waiting_period": "30 days initial (36 months for pre-existing chronic kidney disease)",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Nephrologist Prescription", "KFT Blood Test Reports", "Dialysis Cycle Sheet"],
        "guidance": "Day care treatment covered without 24-hour hospitalization."
    },
    "Maternity Normal Delivery": {
        "estimated_cost": 50000,
        "sub_limit": "INR 50,000 max maternity cap",
        "waiting_period": "24 to 36 months continuous coverage",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Obstetrician ANC Notes", "USG Scan Reports", "Discharge Summary & Birth Certificate"],
        "guidance": "Check if newborn baby cover is included from Day 1 or after 90 days."
    },
    "Maternity C-Section Delivery": {
        "estimated_cost": 75000,
        "sub_limit": "INR 75,000 max maternity cap",
        "waiting_period": "24 to 36 months continuous coverage",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Obstetrician Notes", "USG Scan Reports", "C-Section Surgical Notes & Birth Certificate"],
        "guidance": "C-Section delivery sub-limit cap applies as per policy schedule."
    },
    "Hysterectomy (Uterus Removal)": {
        "estimated_cost": 130000,
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Pelvic USG / MRI Report", "Gynecologist Recommendation", "Histopathology Report"],
        "guidance": "Requires minimum 24-48 hours inpatient admission. Subject to 24-month waiting period."
    },
    "Brain Tumor Craniotomy Surgery": {
        "estimated_cost": 550000,
        "sub_limit": "Up to Base Sum Insured (ICU Covered 100%)",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Brain MRI / CT Scan Report", "Neurosurgeon OT Notes", "ICU Monitoring Summary"],
        "guidance": "Critical neurosurgical care. ICU stays covered without room capping."
    }
}

def get_procedure_details(procedure_name: str) -> Dict[str, Any]:
    return PROCEDURE_DATABASE.get(procedure_name, {
        "estimated_cost": 150000,
        "sub_limit": "As per base policy sum insured",
        "waiting_period": "30 days initial, 24 months specific illness",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Consultation Note", "Diagnostic Test Report", "Itemized Final Bill"],
        "guidance": "Ensure pre-authorization is submitted prior to admission."
    })
