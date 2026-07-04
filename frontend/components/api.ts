export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export async function getDemo() {
  const res = await fetch(`${API_BASE}/api/demo/run`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch demo data');
  return res.json();
}

export async function getReport() {
  const res = await fetch(`${API_BASE}/api/report/markdown`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to fetch report');
  return res.text();
}
