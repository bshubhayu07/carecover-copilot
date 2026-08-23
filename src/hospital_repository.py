import os
import csv
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "data", "hospitals.csv")

def load_hospitals(file_path: str = None) -> List[Dict[str, Any]]:
    """Loads the synthetic hospital dataset using built-in csv module."""
    if file_path is None:
        file_path = DEFAULT_CSV_PATH
        
    if not os.path.exists(file_path):
        if os.path.exists("data/hospitals.csv"):
            file_path = "data/hospitals.csv"
        elif os.path.exists("carecover-copilot/data/hospitals.csv"):
            file_path = "carecover-copilot/data/hospitals.csv"
        else:
            return []

    hospitals = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hospitals.append(dict(row))
            
    return hospitals

def get_all_cities(file_path: str = None) -> list:
    """Returns a sorted list of unique cities available in the dataset."""
    hospitals = load_hospitals(file_path)
    if not hospitals:
        return ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
    cities = sorted(list(set(row['city'].strip() for row in hospitals if row.get('city'))))
    return cities

def get_hospitals_by_city(city: str, file_path: str = None) -> List[Dict[str, Any]]:
    hospitals = load_hospitals(file_path)
    if not hospitals:
        return []
    
    target_city = city.strip().lower()
    return [h for h in hospitals if h.get('city', '').strip().lower() == target_city]
