import { API_BASE } from './api';

interface SldViewerProps {
  sessionId?: string;
}

export default function SldViewer({ sessionId }: SldViewerProps) {
  const pdfUrl = sessionId 
    ? `${API_BASE}/api/sld/pdf?session_id=${sessionId}` 
    : `${API_BASE}/api/sld/pdf`;
  return <div className="card"><h2>Single-line diagram visual reference</h2><iframe className="pdf-frame" src={pdfUrl} /></div>;
}
