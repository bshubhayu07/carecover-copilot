from pydantic import BaseModel, Field
from typing import List, Optional

class Evidence(BaseModel):
    field: str = Field(description="The field this evidence supports")
    page: Optional[int] = Field(description="Page number where the evidence is found")
    quote: str = Field(description="Exact quote from the policy text")

class PolicyProfile(BaseModel):
    insurer_name: Optional[str] = Field(None, description="Name of the insurance company")
    policy_name: Optional[str] = Field(None, description="Name of the policy")
    sum_insured_inr: Optional[float] = Field(None, description="Total sum insured in INR")
    room_eligibility: Optional[str] = Field(None, description="Types of rooms eligible (e.g., General, Twin Sharing, Private)")
    room_rent_limit: Optional[str] = Field(None, description="Limits or capping on the room rent")
    co_pay: Optional[str] = Field(None, description="Co-payment terms if any")
    waiting_periods: List[str] = Field(default_factory=list, description="List of waiting periods mentioned")
    exclusions: List[str] = Field(default_factory=list, description="List of conditions/treatments not covered")
    pre_authorization_required: Optional[bool] = Field(None, description="Is pre-authorization required for planned hospitalizations?")
    network_hospital_terms: Optional[str] = Field(None, description="Terms related to network hospitals")
    claim_documents: List[str] = Field(default_factory=list, description="Documents required for claiming reimbursement")
    evidence: List[Evidence] = Field(default_factory=list, description="Evidence quotes supporting the extracted fields")
