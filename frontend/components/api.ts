const configuredApiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

export const API_BASE = configuredApiBase || (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : '');

function apiUrl(path: string) {
  if (!API_BASE) {
    throw new Error('NEXT_PUBLIC_API_BASE_URL is not configured in this frontend build.');
  }
  return `${API_BASE}${path}`;
}

async function readError(res: Response, fallback: string) {
  const body = await res.json().catch(() => null);
  if (body?.detail) {
    return typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
  }
  return `${fallback} (${res.status})`;
}

export async function uploadFiles(formData: FormData): Promise<{ session_id: string; files: { consumer_list: string; sld_pdf: string } }> {
  const res = await fetch(apiUrl('/api/upload'), {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    throw new Error(await readError(res, 'Upload failed'));
  }
  return res.json();
}

export async function analyzeSession(sessionId: string) {
  const res = await fetch(apiUrl(`/api/analyze?session_id=${sessionId}`), {
    method: 'POST',
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(await readError(res, 'Analysis failed'));
  return res.json();
}

export async function getReport(sessionId?: string) {
  const qs = sessionId ? `?session_id=${sessionId}` : '';
  const res = await fetch(apiUrl(`/api/report/markdown${qs}`), { cache: 'no-store' });
  if (!res.ok) throw new Error(await readError(res, 'Failed to fetch report'));
  return res.text();
}
