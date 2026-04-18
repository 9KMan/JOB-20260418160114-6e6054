export interface Document {
  id: string;
  filename: string;
  file_path: string;
  ocr_text: string | null;
  extracted_data: Record<string, any>;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
}

export interface Entry {
  id: string;
  type: 'text' | 'voice' | 'document';
  content: string;
  source_document_id: string | null;
  metadata: Record<string, any>;
  created_at: string;
}

export interface Transaction {
  id: string;
  entry_id: string;
  amount: number;
  category: string;
  description: string;
  date: string;
  created_at: string;
}

export interface TransactionSummary {
  total_amount: number;
  transaction_count: number;
  by_category: Record<string, number>;
  by_month: Record<string, number>;
}

export interface TranscriptionResult {
  text: string;
  language: string | null;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
