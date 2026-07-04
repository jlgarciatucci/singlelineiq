import { API_BASE } from './api';
export default function SldViewer() {
  return <div className="card"><h2>Single-line diagram visual reference</h2><iframe className="pdf-frame" src={`${API_BASE}/api/sld/pdf`} /></div>;
}
