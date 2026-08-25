import type { PolicyClauses } from '../types/policy';
import type { Hospital } from '../types/hospital';
import type { QAResponsePayload } from '../types/chat';

export async function extractPolicyPDF(file: File): Promise<PolicyClauses> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch('/api/extract-policy', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Policy extraction failed: ${response.statusText}`);
  }

  return response.json();
}

export async function askPolicyQuestion(question: string, language: string): Promise<QAResponsePayload> {
  const response = await fetch('/api/qa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, language }),
  });

  if (!response.ok) {
    throw new Error(`QA query failed: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchHospitals(
  city: string,
  specialty: string,
  inNetworkOnly: boolean,
  userLat?: number | null,
  userLon?: number | null
): Promise<Hospital[]> {
  const params = new URLSearchParams({
    city,
    specialty,
    in_network_only: String(inNetworkOnly)
  });

  if (userLat != null && userLon != null) {
    params.append('user_lat', String(userLat));
    params.append('user_lon', String(userLon));
  }

  const response = await fetch(`/api/hospitals?${params.toString()}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch hospitals: ${response.statusText}`);
  }

  return response.json();
}

export async function purgeSessionData(): Promise<{ message: string }> {
  const response = await fetch('/api/purge-session', { method: 'POST' });
  if (!response.ok) {
    throw new Error(`Failed to purge session: ${response.statusText}`);
  }
  return response.json();
}
