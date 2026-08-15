import pandas as pd
from typing import Dict, Any, List

def match_hospitals(hospitals_df: pd.DataFrame, policy_profile, context_city: str) -> List[Dict[str, Any]]:
    """
    Deterministic eligibility and ranking engine for hospitals.
    Ranking signals:
    1. Network match (In-Network vs Out-of-Network)
    2. Room eligibility match (General, Twin Sharing, Single Private, Suite)
    3. Location/Distance
    """
    if hospitals_df.empty:
        return []
        
    results = []
    
    for _, row in hospitals_df.iterrows():
        # City Match
        if context_city and row['city'].strip().lower() != context_city.strip().lower():
            continue
            
        score = 0
        explanation = []
        network_status = "Out of Network"
        
        # 1. Flexible Network Match
        policy_insurer = policy_profile.insurer_name if (policy_profile and policy_profile.insurer_name) else "DemoCare"
        p_insurer_lower = policy_insurer.lower()
        h_insurers_lower = str(row['network_insurers']).lower() if pd.notna(row['network_insurers']) else ""
        
        # Check direct substring or insurance brand keywords
        is_in_network = False
        if p_insurer_lower in h_insurers_lower:
            is_in_network = True
        elif ("bupa" in p_insurer_lower or "niva" in p_insurer_lower) and ("bupa" in h_insurers_lower or "niva" in h_insurers_lower or "democare" in h_insurers_lower or "healthplus" in h_insurers_lower):
            is_in_network = True
        elif "star" in p_insurer_lower and ("star" in h_insurers_lower or "democare" in h_insurers_lower):
            is_in_network = True
        elif "hdfc" in p_insurer_lower and ("hdfc" in h_insurers_lower or "democare" in h_insurers_lower):
            is_in_network = True
        elif "icici" in p_insurer_lower and ("icici" in h_insurers_lower or "democare" in h_insurers_lower):
            is_in_network = True
        elif "democare" in p_insurer_lower or p_insurer_lower == "uploaded policy":
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
        
        # Check keyword overlaps (e.g. private, twin, general, single, suite, no capping)
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
            
        # 3. Distance 
        distance = row.get('distance_km_demo', 999)
        if pd.notna(distance):
            dist_score = max(0, 20 - int(distance))
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
            "distance": distance,
            "explanation": " | ".join(explanation),
            "caveat": caveat
        })
        
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results
