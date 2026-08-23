import math
from typing import Dict, Any, List

CITY_COORDINATES = {
    'pune': (18.5204, 73.8567),
    'bhubaneswar': (20.2961, 85.8245),
    'bengaluru': (12.9716, 77.5946),
    'mumbai': (19.0760, 72.8777),
    'delhi': (28.6139, 77.2090),
    'delhi ncr': (28.6139, 77.2090),
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
    hospitals: Any, 
    policy_profile, 
    context_city: str, 
    user_city: str = None, 
    use_live_location: bool = False
) -> List[Dict[str, Any]]:
    """
    Deterministic eligibility and ranking engine for hospitals.
    Accepts List of Dicts or DataFrames.
    """
    if hospitals is None:
        return []

    if hasattr(hospitals, 'empty') and hospitals.empty:
        return []

    if not hasattr(hospitals, 'empty') and len(hospitals) == 0:
        return []
        
    results = []
    
    # Handle both List[Dict] and DataFrame inputs
    rows = hospitals.to_dict('records') if hasattr(hospitals, 'to_dict') else hospitals

    for row in rows:
        hosp_city = str(row['city']).strip()
        score = 50
        explanation = []
        
        # 1. Network Matching
        network_insurers = [i.strip().lower() for i in str(row['network_insurers']).split('|')]
        insurer_name = policy_profile.insurer_name if policy_profile else "Niva Bupa"
        
        if any(ins in insurer_name.lower() for ins in network_insurers) or "all" in network_insurers:
            score += 30
            network_status = "In Network"
            explanation.append(f"Direct cashless network partner with {insurer_name}.")
        else:
            score -= 20
            network_status = "Out of Network"
            explanation.append(f"Not in direct cashless network for {insurer_name}. Reimbursement claim required.")
            
        # 2. Room Eligibility Matching
        policy_room = policy_profile.room_eligibility if policy_profile else "Single Private Room"
        policy_rooms = [r.strip().lower() for r in policy_room.split('/')]
        hosp_rooms = [r.strip().lower() for r in str(row['room_types']).split('|')]
        
        has_room_match = False
        matching_types = []
        p_room_lower = policy_room.lower()
        
        for pr in policy_rooms:
            for hr in hosp_rooms:
                if pr in hr or hr in pr:
                    has_room_match = True
                    matching_types.append(hr.title())
            
        if has_room_match or "no capping" in p_room_lower or "single private" in p_room_lower:
            score += 30
            room_desc = matching_types[0] if matching_types else "Single Private Room"
            explanation.append(f"Room Match: Covered for {room_desc}.")
            eligible_room_display = room_desc
        else:
            explanation.append(f"Room Warning: Policy covers {policy_rooms}, but hospital offers {hosp_rooms}.")
            eligible_room_display = "Requires out-of-pocket upgrade"
            
        # 3. Dynamic Distance Calculation
        local_demo_dist = float(row.get('distance_km_demo', 5.0))
        
        if use_live_location and user_city:
            u_city_clean = user_city.strip().lower()
            h_city_clean = hosp_city.strip().lower()
            
            if u_city_clean in CITY_COORDINATES and h_city_clean in CITY_COORDINATES:
                u_lat, u_lon = CITY_COORDINATES[u_city_clean]
                h_lat, h_lon = CITY_COORDINATES[h_city_clean]
                
                if u_city_clean == h_city_clean:
                    computed_dist = local_demo_dist
                else:
                    inter_city_km = calculate_haversine(u_lat, u_lon, h_lat, h_lon)
                    computed_dist = round(inter_city_km + local_demo_dist, 1)
            else:
                computed_dist = local_demo_dist
        else:
            computed_dist = local_demo_dist
            
        dist_score = max(0, 20 - int(computed_dist / 10 if computed_dist > 50 else computed_dist))
        score += dist_score
            
        caveat = "Verify with insurer/hospital before admission."
        if policy_profile and policy_profile.pre_authorization_required:
            caveat += " Pre-authorization required."
            
        feed_id = f"FEED-{(policy_profile.insurer_name if policy_profile else 'NIVABUPA').upper().replace(' ', '')}-20260816-01"

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
            "caveat": caveat,
            "feed_id": feed_id
        })
        
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
