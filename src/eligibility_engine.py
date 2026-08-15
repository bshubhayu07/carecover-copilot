import math
import pandas as pd
from typing import Dict, Any, List

CITY_COORDINATES = {
    'pune': (18.5204, 73.8567),
    'bhubaneswar': (20.2961, 85.8245),
    'bengaluru': (12.9716, 77.5946),
    'mumbai': (19.0760, 72.8777),
    'delhi': (28.6139, 77.2090),
    'chennai': (13.0827, 80.2707),
    'kolkata': (22.5726, 88.3639),
    'hyderabad': (17.3850, 78.4867),
    'ahmedabad': (23.0225, 72.5714),
    'jaipur': (26.9124, 75.7873),
    'lucknow': (26.8467, 80.9462),
    'chandigarh': (30.7333, 76.7794),
    'kochi': (9.9312, 76.2673),
    'bhopal': (23.2599, 77.4126),
    'patna': (25.5941, 85.1376),
    'guwahati': (26.1445, 91.7362)
}

def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def match_hospitals(
    hospitals_df: pd.DataFrame, 
    policy_profile, 
    context_city: str, 
    user_city: str = None, 
    use_live_location: bool = False
) -> List[Dict[str, Any]]:
    """
    Deterministic eligibility and ranking engine for hospitals.
    Calculates exact inter-city and intra-city distances when user location permission is enabled.
    """
    if hospitals_df.empty:
        return []
        
    results = []
    
    for _, row in hospitals_df.iterrows():
        hosp_city = str(row['city']).strip()
        
        score = 0
        explanation = []
        network_status = "Out of Network"
        
        # 1. Flexible Network Match
        policy_insurer = policy_profile.insurer_name if (policy_profile and policy_profile.insurer_name) else "DemoCare"
        p_insurer_lower = policy_insurer.lower()
        h_insurers_lower = str(row['network_insurers']).lower() if pd.notna(row['network_insurers']) else ""
        
        is_in_network = False
        if p_insurer_lower in h_insurers_lower:
            is_in_network = True
        elif ("bupa" in p_insurer_lower or "niva" in p_insurer_lower) and ("bupa" in h_insurers_lower or "niva" in h_insurers_lower):
            is_in_network = True
        elif "star" in p_insurer_lower and "star" in h_insurers_lower:
            is_in_network = True
        elif "hdfc" in p_insurer_lower and "hdfc" in h_insurers_lower:
            is_in_network = True
        elif "icici" in p_insurer_lower and "icici" in h_insurers_lower:
            is_in_network = True
        elif "democare" in p_insurer_lower and "democare" in h_insurers_lower:
            is_in_network = True
            
        if is_in_network:
            score += 50
            network_status = "In Network"
            explanation.append(f"Network Match: In-Network for {policy_insurer}.")
        else:
            explanation.append(f"Out of Network for {policy_insurer} (Subject to deductions).")
            
        # 2. Flexible Room Match
        policy_rooms = policy_profile.room_eligibility if (policy_profile and policy_profile.room_eligibility) else "General"
        p_room_lower = policy_rooms.lower()
        hosp_rooms = str(row['room_types']) if pd.notna(row['room_types']) else ""
        h_rooms_lower = hosp_rooms.lower()
        
        has_room_match = False
        matching_types = []
        
        if "private" in p_room_lower or "no capping" in p_room_lower or "no room rent limit" in p_room_lower:
            if "private" in h_rooms_lower or "twin" in h_rooms_lower or "general" in h_rooms_lower:
                has_room_match = True
                matching_types.append("Single Private Room")
        if "twin" in p_room_lower and ("twin" in h_rooms_lower or "general" in h_rooms_lower):
            has_room_match = True
            matching_types.append("Twin Sharing")
        if "general" in p_room_lower and "general" in h_rooms_lower:
            has_room_match = True
            matching_types.append("General Ward")
            
        if has_room_match or "no capping" in p_room_lower or "single private" in p_room_lower:
            score += 30
            room_desc = matching_types[0] if matching_types else "Single Private Room"
            explanation.append(f"Room Match: Covered for {room_desc}.")
            eligible_room_display = room_desc
        else:
            explanation.append(f"Room Warning: Policy covers {policy_rooms}, but hospital offers {hosp_rooms}.")
            eligible_room_display = "Requires out-of-pocket upgrade"
            
        # 3. Dynamic Distance Calculation (Inter-city vs Intra-city)
        local_demo_dist = float(row.get('distance_km_demo', 5.0))
        
        if use_live_location and user_city:
            u_city_clean = user_city.strip().lower()
            h_city_clean = hosp_city.strip().lower()
            
            if u_city_clean in CITY_COORDINATES and h_city_clean in CITY_COORDINATES:
                u_lat, u_lon = CITY_COORDINATES[u_city_clean]
                h_lat, h_lon = CITY_COORDINATES[h_city_clean]
                
                if u_city_clean == h_city_clean:
                    # Same city: use intra-city landmark distance
                    computed_dist = local_demo_dist
                else:
                    # Inter-city distance calculation using Haversine formula
                    inter_city_km = calculate_haversine(u_lat, u_lon, h_lat, h_lon)
                    computed_dist = round(inter_city_km + local_demo_dist, 1)
            else:
                computed_dist = local_demo_dist
        else:
            computed_dist = local_demo_dist
            
        # Add distance scoring
        dist_score = max(0, 20 - int(computed_dist / 10 if computed_dist > 50 else computed_dist))
        score += dist_score
            
        caveat = "Verify with insurer/hospital before admission."
        if policy_profile and policy_profile.pre_authorization_required:
            caveat += " Pre-authorization required."
            
        results.append({
            "id": row['hospital_id'],
            "name": row['hospital_name'],
            "city": row['city'],
            "specialties": row['specialties'],
            "score": score,
            "network_status": network_status,
            "eligible_room": eligible_room_display,
            "distance": computed_dist,
            "explanation": " | ".join(explanation),
            "caveat": caveat
        })
        
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
