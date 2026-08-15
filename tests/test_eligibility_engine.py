import pandas as pd
from src.eligibility_engine import match_hospitals
from src.policy_schema import PolicyProfile

def test_hospital_ranking():
    hospitals_data = {
        'hospital_id': ['H1', 'H2'],
        'hospital_name': ['A', 'B'],
        'city': ['Bengaluru', 'Bengaluru'],
        'specialties': ['Gen', 'Gen'],
        'network_insurers': ['DemoCare', 'Other'],
        'room_types': ['General|Private', 'General'],
        'distance_km_demo': [10, 5]
    }
    df = pd.DataFrame(hospitals_data)
    
    policy = PolicyProfile(
        insurer_name="DemoCare",
        room_eligibility="Private"
    )
    
    results = match_hospitals(df, policy, "Bengaluru")
    
    assert len(results) == 2
    # H1 should rank higher because it is in-network and has the room match, despite being further
    assert results[0]['id'] == 'H1'
    assert results[0]['network_status'] == 'In Network'
    assert "Private" in results[0]['eligible_room']
    
    assert results[1]['id'] == 'H2'
    assert results[1]['network_status'] == 'Out of Network'
