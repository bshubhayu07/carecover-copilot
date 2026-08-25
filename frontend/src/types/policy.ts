export interface PolicyClauses {
  insurer_name: string;
  sum_insured_inr: number;
  room_eligibility: string;
  co_payment_percentage: number;
  pre_authorization_required: boolean;
  maternity_covered?: boolean;
  cataract_sublimit_inr?: number;
}

export interface CombinedCoverage {
  primary_base_si: number;
  super_topup_si: number;
  combined_total_si: number;
}
