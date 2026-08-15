import pandas as pd
import os

def load_hospitals(file_path: str = "carecover-copilot/data/hospitals.csv") -> pd.DataFrame:
    """Loads the synthetic hospital dataset."""
    if not os.path.exists(file_path):
        return pd.DataFrame()
    return pd.read_csv(file_path)

def get_hospitals_by_city(city: str, file_path: str = "carecover-copilot/data/hospitals.csv") -> pd.DataFrame:
    df = load_hospitals(file_path)
    if df.empty:
        return df
    
    # Simple case-insensitive filter
    return df[df['city'].str.lower() == city.lower()]
