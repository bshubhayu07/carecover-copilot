import os
import csv
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "data", "hospitals.csv")

FALLBACK_HOSPITALS = [
    {"name": "Apollo Super Speciality (Saket)", "city": "Delhi", "specialties": "Cardiology, Orthopedics, Oncology", "network_status": "In Network", "latitude": 28.5244, "longitude": 77.2167, "address": "Saket, Delhi", "emergency_available": "Yes", "feed_id": "FEED-DELHI-01"},
    {"name": "Manipal Super Speciality (Rajinder Nagar)", "city": "Delhi", "specialties": "Orthopedics, Neurology, Multispecialty", "network_status": "In Network", "latitude": 28.6402, "longitude": 77.1798, "address": "Rajinder Nagar, Delhi", "emergency_available": "Yes", "feed_id": "FEED-DELHI-02"},
    {"name": "Fortis Super Speciality (Okhla)", "city": "Delhi", "specialties": "Cardiology, Orthopedics, Multispecialty", "network_status": "In Network", "latitude": 28.5562, "longitude": 77.2778, "address": "Okhla, Delhi", "emergency_available": "Yes", "feed_id": "FEED-DELHI-03"},
    {"name": "Apollo Super Speciality (Sassoon Road)", "city": "Pune", "specialties": "Cardiology, Orthopedics, Oncology", "network_status": "In Network", "latitude": 18.5204, "longitude": 73.8567, "address": "Sassoon Road, Pune", "emergency_available": "Yes", "feed_id": "FEED-PUNE-01"},
    {"name": "Manipal Super Speciality (Deccan Gymkhana)", "city": "Pune", "specialties": "Orthopedics, Neurology, Multispecialty", "network_status": "In Network", "latitude": 18.5167, "longitude": 73.8412, "address": "Deccan Gymkhana, Pune", "emergency_available": "Yes", "feed_id": "FEED-PUNE-02"},
    {"name": "Fortis Super Speciality (Kharadi)", "city": "Mumbai", "specialties": "Cardiology, Oncology, Multispecialty", "network_status": "In Network", "latitude": 19.0760, "longitude": 72.8777, "address": "Kharadi, Mumbai", "emergency_available": "Yes", "feed_id": "FEED-MUMBAI-01"},
    {"name": "Narayana Health (Electronic City)", "city": "Bengaluru", "specialties": "Cardiology, Oncology, Multispecialty", "network_status": "In Network", "latitude": 12.9716, "longitude": 77.5946, "address": "Electronic City, Bengaluru", "emergency_available": "Yes", "feed_id": "FEED-BLR-01"},
    {"name": "Yashoda Hospital (Somajiguda)", "city": "Hyderabad", "specialties": "Cardiology, Orthopedics, Multispecialty", "network_status": "In Network", "latitude": 17.3850, "longitude": 78.4867, "address": "Somajiguda, Hyderabad", "emergency_available": "Yes", "feed_id": "FEED-HYD-01"},
    {"name": "MIOT International (Manapakkam)", "city": "Chennai", "specialties": "Orthopedics, Cardiology, Multispecialty", "network_status": "In Network", "latitude": 13.0827, "longitude": 80.2707, "address": "Manapakkam, Chennai", "emergency_available": "Yes", "feed_id": "FEED-CHE-01"},
    {"name": "AMRI Hospital (Dhakuria)", "city": "Kolkata", "specialties": "Cardiology, Oncology, Multispecialty", "network_status": "In Network", "latitude": 22.5726, "longitude": 88.3639, "address": "Dhakuria, Kolkata", "emergency_available": "Yes", "feed_id": "FEED-KOL-01"},
    {"name": "Zydus Hospital (Thaltej)", "city": "Ahmedabad", "specialties": "Cardiology, Orthopedics, Multispecialty", "network_status": "In Network", "latitude": 23.0225, "longitude": 72.5714, "address": "Thaltej, Ahmedabad", "emergency_available": "Yes", "feed_id": "FEED-AMD-01"}
]

CITY_ALIAS_MAP = {
    "delhi ncr": "Delhi",
    "new delhi": "Delhi",
    "noida": "Delhi",
    "gurugram": "Delhi",
    "faridabad": "Delhi",
    "bengaluru": "Bengaluru",
    "bangalore": "Bengaluru",
    "chhatrapati sambhajinagar": "Aurangabad"
}

def load_hospitals(file_path: str = None) -> List[Dict[str, Any]]:
    """Loads hospital dataset with fallback synthetic data."""
    if file_path is None:
        file_path = DEFAULT_CSV_PATH
        
    if not os.path.exists(file_path):
        if os.path.exists("data/hospitals.csv"):
            file_path = "data/hospitals.csv"
        elif os.path.exists("carecover-copilot/data/hospitals.csv"):
            file_path = "carecover-copilot/data/hospitals.csv"
        else:
            return FALLBACK_HOSPITALS

    hospitals = []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hospitals.append(dict(row))
    except Exception:
        return FALLBACK_HOSPITALS
            
    return hospitals if hospitals else FALLBACK_HOSPITALS

def get_all_cities(file_path: str = None) -> list:
    """Returns a sorted list of unique cities available in the dataset."""
    hospitals = load_hospitals(file_path)
    cities = sorted(list(set(row['city'].strip() for row in hospitals if row.get('city'))))
    return cities if cities else ["Pune", "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Ahmedabad"]

def generate_city_hospitals(city_name: str) -> List[Dict[str, Any]]:
    city_title = city_name.strip().title()
    templates = [
        ("Apollo Super Speciality (Civil Lines)", "General|Cardiology|Orthopedics|Multispecialty", "3520", "1.8"),
        ("Manipal Super Speciality (VIP Road)", "Oncology|Neurology|Cardiology|Multispecialty", "4500", "2.4"),
        ("Fortis Super Speciality (Station Road)", "Orthopedics|Neurology|Multispecialty", "4200", "3.0"),
        ("Dr. Agarwal Eye Hospital & Laser Center", "Ophthalmology|Eye Care|Laser Surgery", "3200", "1.5"),
        ("Max Super Speciality (Shankar Nagar)", "Cardiology|Oncology|Multispecialty", "4800", "3.6"),
        ("Narayana Health Super Speciality (Pandri)", "Gastroenterology|Urology|Multispecialty", "3900", "4.2"),
        ("Aster Super Speciality (Telibandha)", "Pulmonology|Gynecology|Obstetrics|Multispecialty", "4100", "4.8"),
        ("KIMS Super Speciality (Ring Road)", "Pediatrics|Ophthalmology|Multispecialty", "3800", "5.4"),
        ("Yashoda Super Speciality (Main Market)", "ENT|Multispecialty|Orthopedics", "3600", "6.0"),
        ("PulmoCare Respiratory & Chest Center", "Pulmonology|Respiratory Care|Multispecialty", "4500", "2.2"),
        ("Kidney & Urology Super Speciality Center", "Urology|Nephrology|Kidney Care|Multispecialty", "4800", "2.8"),
        ("Columbia Asia Super Speciality (New Town)", "Cardiology|Neurology|Multispecialty", "4400", "6.6"),
        ("Sahyadri Super Speciality (Bypass)", "Oncology|Urology|Obstetrics|Multispecialty", "4000", "7.2")
    ]
    hospitals = []
    for idx, (name_tmpl, spec, cost, dist) in enumerate(templates, 1):
        parts = name_tmpl.split("(")
        base_name = parts[0].strip()
        locality = parts[1].replace(")", "").strip() if len(parts) > 1 else "Central"
        hospitals.append({
            "hospital_id": f"H_{city_title.upper()[:3]}_{idx:03d}",
            "hospital_name": f"{base_name} ({locality}, {city_title})",
            "city": city_title,
            "specialties": spec,
            "network_insurers": "Niva Bupa|Star Health|HDFC ERGO|ICICI Lombard|Care Health|DemoCare|HealthPlus",
            "room_types": "General|Twin Sharing|Private",
            "indicative_daily_room_cost_inr": cost,
            "indicative_procedure_cost_band": "Low",
            "emergency_available": "Yes",
            "distance_km_demo": dist
        })
    return hospitals

def get_hospitals_by_city(city: str, file_path: str = None) -> List[Dict[str, Any]]:
    hospitals = load_hospitals(file_path)
    normalized_city = CITY_ALIAS_MAP.get(city.lower().strip(), city.strip())
    
    matched = [h for h in hospitals if h.get('city', '').lower().strip() == normalized_city.lower().strip()]
    if not matched:
        # Fallback search matching substrings
        matched = [h for h in hospitals if normalized_city.lower().strip() in h.get('city', '').lower().strip()]
        
    return matched if matched else generate_city_hospitals(city)
