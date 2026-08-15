import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "data", "hospitals.csv")

def load_hospitals(file_path: str = None) -> pd.DataFrame:
    """Loads the synthetic hospital dataset."""
    if file_path is None:
        file_path = DEFAULT_CSV_PATH
        
    if not os.path.exists(file_path):
        # Fallback check relative to CWD
        if os.path.exists("data/hospitals.csv"):
            file_path = "data/hospitals.csv"
        elif os.path.exists("carecover-copilot/data/hospitals.csv"):
            file_path = "carecover-copilot/data/hospitals.csv"
        else:
            return pd.DataFrame()
            
    return pd.read_csv(file_path)

def get_all_cities(file_path: str = None) -> list:
    """Returns a sorted list of unique cities available in the dataset."""
    df = load_hospitals(file_path)
    if df.empty or 'city' not in df.columns:
        return ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
    cities = sorted(df['city'].dropna().unique().tolist())
    return cities

def get_hospitals_by_city(city: str, file_path: str = None) -> pd.DataFrame:
    df = load_hospitals(file_path)
    if df.empty:
        return df
    
    # Case-insensitive filter
    return df[df['city'].str.strip().str.lower() == city.strip().lower()]
