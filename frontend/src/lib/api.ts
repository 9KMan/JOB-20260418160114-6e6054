const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function fetchApi(endpoint: string, options?: RequestInit) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

// Voice endpoints
export const transcribeAudio = async (file: File): Promise<{ text: string }> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/api/voice/transcribe`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Transcription failed: ${response.status}`);
  }

  return response.json();
};

// Document endpoints
export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/api/documents/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.status}`);
  }

  return response.json();
};

export const listDocuments = async () => {
  return fetchApi('/api/documents/');
};

export const deleteDocument = async (id: string) => {
  return fetchApi(`/api/documents/${id}`, { method: 'DELETE' });
};

// Entry endpoints
export const createEntry = async (data: { type: string; content: string; metadata?: object }) => {
  return fetchApi('/api/entries/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const listEntries = async (type?: string) => {
  const params = type ? `?entry_type=${type}` : '';
  return fetchApi(`/api/entries/${params}`);
};

export const deleteEntry = async (id: string) => {
  return fetchApi(`/api/entries/${id}`, { method: 'DELETE' });
};

// Transaction endpoints
export const createTransaction = async (data: {
  entry_id: string;
  amount: number;
  category: string;
  description: string;
  date: string;
}) => {
  return fetchApi('/api/transactions/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
};

export const listTransactions = async (params?: {
  category?: string;
  start_date?: string;
  end_date?: string;
}) => {
  const queryParams = new URLSearchParams();
  if (params?.category) queryParams.append('category', params.category);
  if (params?.start_date) queryParams.append('start_date', params.start_date);
  if (params?.end_date) queryParams.append('end_date', params.end_date);
  const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return fetchApi(`/api/transactions/${query}`);
};

export const getTransactionSummary = async (params?: { start_date?: string; end_date?: string }) => {
  const queryParams = new URLSearchParams();
  if (params?.start_date) queryParams.append('start_date', params.start_date);
  if (params?.end_date) queryParams.append('end_date', params.end_date);
  const query = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return fetchApi(`/api/transactions/summary${query}`);
};

export const deleteTransaction = async (id: string) => {
  return fetchApi(`/api/transactions/${id}`, { method: 'DELETE' });
};
