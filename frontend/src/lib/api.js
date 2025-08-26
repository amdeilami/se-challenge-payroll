const API_BASE = import.meta.env.VITE_API_BASE || '/api';

/** Upload CSV (multipart/form-data with field name "file") */
export async function uploadTimesheet(file) {
  const fd = new FormData();
  fd.append('file', file); // backend expects "file"
  const res = await fetch(`${API_BASE}/timesheets/upload`, {
    method: 'POST',
    body: fd,
  });
  return parseResponse(res);
}

/** Fetch payroll report (JSON) for a date range */
export async function fetchPayroll({ start, end }) {
  const params = new URLSearchParams({ start, end });
  const res = await fetch(`${API_BASE}/payroll?${params.toString()}`);
  return parseResponse(res);
}

/** Utility: parse JSON if possible; otherwise text, and surface errors */
async function parseResponse(res) {
  const ct = res.headers.get('content-type') || '';
  const isJson = ct.includes('application/json');
  const payload = isJson ? await res.json() : await res.text();
  if (!res.ok) {
    const msg = isJson ? (payload.detail || JSON.stringify(payload)) : payload;
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return payload;
}
