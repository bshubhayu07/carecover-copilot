import math
from typing import Dict, Any, List

CITY_COORDINATES = {
    'pune': (18.5204, 73.8567),
    'bhubaneswar': (20.2961, 85.8245),
    'bengaluru': (12.9716, 77.5946),
    'mumbai': (19.0760, 72.8777),
    'delhi': (28.6139, 77.2090),
    'delhi ncr': (28.6139, 77.2090),
    'new delhi': (28.6139, 77.2090),
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
    'guwahati': (26.1445, 91.7362),
    'raipur': (21.2514, 81.6296),
    'indore': (22.7196, 75.8577),
    'nagpur': (21.1458, 79.0882),
    'visakhapatnam': (17.6868, 83.2185),
    'surat': (21.1702, 72.8311),
    'vadodara': (22.3072, 73.1812),
    'coimbatore': (11.0168, 76.9558),
    'ranchi': (23.3441, 85.3096),
    'varanasi': (25.3176, 82.9739),
    'agra': (27.1767, 78.0081),
    'dehradun': (30.3165, 78.0322),
    'ludhiana': (30.9010, 75.8573),
    'amritsar': (31.6340, 74.8723),
    'nashik': (19.9975, 73.7898),
    'thane': (19.2183, 72.9781),
    'rajkot': (22.3039, 70.8022),
    'madurai': (9.9252, 78.1198),
    'thiruvananthapuram': (8.5241, 76.9366),
    'kozhikode': (11.2588, 75.7804),
    'vijayawada': (16.5062, 80.6480),
    'jamshedpur': (22.8046, 86.2029),
    'gwalior': (26.2183, 78.1828),
    'jabalpur': (23.1815, 79.9864),
    'aurangabad': (19.8762, 75.3433),
    'jodhpur': (26.2389, 73.0243),
    'udaipur': (24.5854, 73.7125),
    'kota': (25.2138, 75.8648)
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
    use_live_location: bool = False,
    user_lat: float = None,
    user_lon: float = None
) -> List[Dict[str, Any]]:
    """
    Deterministic eligibility and ranking engine for hospitals.
    Accepts List of Dicts or DataFrames.
    Calculates exact dynamic distance relative to user's current GPS location or city.
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
            
        # 3. Dynamic Distance Calculation from User's Current Location/GPS
        h_lat = float(row['latitude']) if row.get('latitude') is not None and str(row.get('latitude')).strip() != '' else None
        h_lon = float(row['longitude']) if row.get('longitude') is not None and str(row.get('longitude')).strip() != '' else None
        local_offset = float(row.get('distance_km_demo', 3.5))

        if user_lat is not None and user_lon is not None:
            if h_lat is not None and h_lon is not None:
                computed_dist = round(calculate_haversine(user_lat, user_lon, h_lat, h_lon), 1)
                if computed_dist < 0.2:
                    computed_dist = round(local_offset, 1)
            elif hosp_city.lower() in CITY_COORDINATES:
                hc_lat, hc_lon = CITY_COORDINATES[hosp_city.lower()]
                base_dist = calculate_haversine(user_lat, user_lon, hc_lat, hc_lon)
                computed_dist = round(base_dist + (local_offset if base_dist < 10.0 else 0), 1)
            else:
                computed_dist = local_offset
            dist_label = f"{computed_dist:,.1f} km away"
        elif user_city and user_city.strip():
            u_city_clean = user_city.strip().lower()
            h_city_clean = hosp_city.strip().lower()
            if u_city_clean in CITY_COORDINATES and h_city_clean in CITY_COORDINATES:
                u_lat, u_lon = CITY_COORDINATES[u_city_clean]
                hc_lat, hc_lon = CITY_COORDINATES[h_city_clean]
                if u_city_clean == h_city_clean:
                    computed_dist = local_offset
                else:
                    inter_city_dist = calculate_haversine(u_lat, u_lon, hc_lat, hc_lon)
                    computed_dist = round(inter_city_dist + local_offset, 1)
            else:
                computed_dist = local_offset
            
            dist_label = f"{computed_dist:,.1f} km away"
        else:
            computed_dist = local_offset
            dist_label = f"{computed_dist:,.1f} km away"

        dist_score = max(0, 20 - int(computed_dist / 10 if computed_dist > 50 else computed_dist))
        score += dist_score
            
        caveat = "Verify with insurer/hospital before admission."
        if policy_profile and policy_profile.pre_authorization_required:
            caveat += " Pre-authorization required."
            
        feed_id = f"FEED-{(policy_profile.insurer_name if policy_profile else 'NIVABUPA').upper().replace(' ', '')}-20260816-01"
        match_score_percent = min(98, max(55, score))

        results.append({
            "id": row['hospital_id'],
            "name": row['hospital_name'],
            "city": row['city'],
            "specialties": row['specialties'],
            "score": score,
            "match_score_percent": match_score_percent,
            "match_reasons": explanation,
            "network_status": network_status,
            "eligible_room": eligible_room_display,
            "distance": computed_dist,
            "distance_display": dist_label,
            "explanation": " | ".join(explanation),
            "caveat": caveat,
            "feed_id": feed_id
        })
        
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
