export const API_BASE = 'http://127.0.0.1:8000'; 
// iOS Simulator: keep 127.0.0.1
// Android Emulator: use http://10.0.2.2:8000
// Real phone on same Wi-Fi: http://YOUR-LAPTOP-IP:8000

export async function api(path, method='GET', body=null, token=null) {
  const headers = {'Content-Type': 'application/json'};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  const res = await fetch(`${API_BASE}${path}`, {
    method, headers, body: body ? JSON.stringify(body) : null
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || 'Request failed');
  }
  return res.json();
}
