export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function uploadFiles(formData: FormData): Promise<{ session_id: string; files: { consumer_list: string; sld_pdf: string } }> {
  const res = await fetch(`${API_BASE}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const detail = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(detail.detail || 'Upload failed');
  }
  return res.json();
}

export async function analyzeSession(sessionId: string) {
  const res = await fetch(`${API_BASE}/api/analyze?session_id=${sessionId}`, {
    method: 'POST',
    cache: 'no-store',
  });
  if (!res.ok) throw new Error('Analysis failed');
  return res.json();
}

export async function getReport(sessionId?: string) {
  const qs = sessionId ? `?session_id=${sessionId}` : '';
  const res = await fetch(`${API_BASE}/api/report/markdown${qs}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch report');
  return res.text();
}

export async function getDemo() {
  const res = await fetch(`${API_BASE}/api/demo/run`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch demo data');
  return res.json();
}
