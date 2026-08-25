export type ChatRole = 'user' | 'assistant' | 'system';

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  timestamp: string;
  sources?: string[];
  isError?: boolean;
}

export interface QARequestPayload {
  question: string;
  language?: string;
}

export interface QAResponsePayload {
  answer: string;
  policy_clauses_used?: string[];
  safety_status?: string;
}
