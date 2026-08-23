import pytest
from src.hospital_repository import get_hospitals_by_city, get_all_cities
from src.eligibility_engine import match_hospitals
from src.policy_schema import PolicyProfile

SUPPORTED_CITIES = [
    "Pune",
    "Mumbai",
    "Delhi",
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Ahmedabad"
]

@pytest.mark.parametrize("city", SUPPORTED_CITIES)
def test_every_city_returns_hospitals(city):
    """
    Integration Test: Assert that every supported metro city returns
    at least one valid network hospital from the repository.
    """
    hospitals = get_hospitals_by_city(city)
    assert len(hospitals) > 0, f"Hospital repository returned zero results for city: {city}"
    
    demo_profile = PolicyProfile(insurer_name="Niva Bupa", room_eligibility="Single Room")
    matches = match_hospitals(hospitals, demo_profile, context_city=city, user_city=city, use_live_location=False)
    
    assert len(matches) > 0, f"Match engine returned 0 hospital matches for city: {city}"
    assert 'network_status' in matches[0]
    assert 'feed_id' in matches[0]
