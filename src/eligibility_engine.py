import pandas as pd
from typing import Dict, Any, List

def match_hospitals(hospitals_df: pd.DataFrame, policy_profile, context_city: str) -> List[Dict[str, Any]]:
    """
    Deterministic eligibility and ranking engine for hospitals.
    Ranking signals:
    1. Network match
    2. Room eligibility match
    3. City/location match
    4. Distance (if available)
    """
    if hospitals_df.empty:
        return []
        
    results = []
    
    for _, row in hospitals_df.iterrows():
        # 1. City Match (Hard filter if we want, but we assume it's pre-filtered or ranked)
        if context_city and row['city'].lower() != context_city.lower():
            continue
            
        score = 0
        explanation = []
        network_status = "Out of Network"
        
        # 2. Network Match
        policy_insurer = policy_profile.insurer_name if policy_profile and policy_profile.insurer_name else "DemoCare"
        # Dummy matching heuristic: check if insurer name is in the hospital's accepted insurers string
        if pd.notna(row['network_insurers']) and policy_insurer.lower() in row['network_insurers'].lower():
            score += 50
            network_status = "In Network"
            explanation.append(f"Network Match: Accepts {policy_insurer}.")
        else:
            explanation.append(f"Out of Network for {policy_insurer} (Subject to deductions).")
            
        # 3. Room Eligibility Match
        policy_rooms = policy_profile.room_eligibility if policy_profile and policy_profile.room_eligibility else "General"
        hosp_rooms = row['room_types'] if pd.notna(row['room_types']) else ""
        
        # Check if they have overlapping room types
        policy_rooms_list = [r.strip().lower() for r in policy_rooms.split(',')]
        hosp_rooms_list = [r.strip().lower() for r in hosp_rooms.split('|')]
        
        overlap = set(policy_rooms_list).intersection(set(hosp_rooms_list))
        if overlap:
            score += 30
            explanation.append(f"Room Match: Has eligible rooms ({', '.join(overlap).title()}).")
            eligible_room_display = ', '.join(overlap).title()
        else:
            explanation.append(f"Room Warning: Policy covers {policy_rooms}, but hospital offers {hosp_rooms}.")
            eligible_room_display = "Requires out-of-pocket upgrade"
            
        # 4. Distance 
        distance = row.get('distance_km_demo', 999)
        if pd.notna(distance):
            # Closer is better (add points inversely proportional to distance)
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
