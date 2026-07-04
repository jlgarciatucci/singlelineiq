import { useState, useRef } from 'react';
import { uploadFiles } from './api';

interface UploadPanelProps {
  onUploadSuccess: (sessionId: string, filenames: { consumer_list: string; sld_pdf: string }) => void;
}

export default function UploadPanel({ onUploadSuccess }: UploadPanelProps) {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<{ consumer_list: string; sld_pdf: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const doUpload = async (fileList: FileList | File[]) => {
    const files = Array.from(fileList);
    if (files.length !== 2) {
      setError(`Please select exactly 2 files (Consumer List + SLD PDF). You selected ${files.length}.`);
      return;
    }

    // Validate file types
    const exts = files.map(f => f.name.split('.').pop()?.toLowerCase());
    const hasSpreadsheet = exts.some(e => ['csv', 'xlsx', 'xlsm', 'xls'].includes(e || ''));
    const hasPdf = exts.some(e => e === 'pdf');

    if (!hasSpreadsheet) {
      setError('Missing Consumer List file. Please include a CSV or XLSX file.');
      return;
    }
    if (!hasPdf) {
      setError('Missing SLD PDF file. Please include a PDF file.');
      return;
    }

    setError(null);
    setUploading(true);

    try {
      const formData = new FormData();
      files.forEach(f => formData.append('files', f));
      const result = await uploadFiles(formData);
      setUploadedFiles(result.files);
      onUploadSuccess(result.session_id, result.files);
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      doUpload(e.dataTransfer.files);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      doUpload(e.target.files);
    }
  };

  const handleReset = () => {
    setUploadedFiles(null);
    setError(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className="card" style={{ marginBottom: 16 }}>
      <h2>📂 Upload Engineering Deliverables</h2>
      <p className="muted" style={{ fontSize: 14 }}>
        Upload exactly <strong>two files</strong> to begin your review:
      </p>
      <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
        <span className="badge" style={{ fontSize: 11, padding: '4px 10px' }}>① Consumer List (.csv / .xlsx)</span>
        <span className="badge" style={{ fontSize: 11, padding: '4px 10px' }}>② Single-Line Diagram (.pdf)</span>
      </div>
      
      {!uploadedFiles ? (
        <>
          <div 
            className={`upload-zone ${dragActive ? 'active' : ''}`}
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            style={{
              border: `2px dashed ${dragActive ? 'var(--accent)' : 'rgba(45, 212, 255, 0.4)'}`,
              borderRadius: 12,
              padding: 24,
              textAlign: 'center',
              background: dragActive ? 'rgba(45, 212, 255, 0.08)' : 'rgba(14, 26, 45, 0.4)',
              cursor: uploading ? 'wait' : 'pointer',
              transition: 'all 0.2s ease',
              marginBottom: 12,
              opacity: uploading ? 0.6 : 1,
            }}
          >
            <input 
              ref={inputRef}
              type="file" 
              id="file-upload" 
              multiple
              accept=".csv,.xlsx,.xlsm,.xls,.pdf"
              onChange={handleFileInput} 
              style={{ display: 'none' }}
              disabled={uploading}
            />
            <label htmlFor="file-upload" style={{ cursor: uploading ? 'wait' : 'pointer' }}>
              {uploading ? (
                <>
                  <div style={{ fontSize: 28, marginBottom: 8 }}>⏳</div>
                  <strong>Uploading files...</strong>
                </>
              ) : (
                <>
                  <div style={{ fontSize: 32, marginBottom: 8 }}>📁</div>
                  <strong>Drag & drop your two files here</strong>
                  <span style={{ display: 'block', color: 'var(--muted)', fontSize: 13, marginTop: 4 }}>
                    or click to browse (.csv, .xlsx, .pdf)
                  </span>
                </>
              )}
            </label>
          </div>

          {error && (
            <div style={{ 
              padding: '10px 14px', 
              background: 'rgba(255, 100, 100, 0.1)', 
              borderLeft: '4px solid var(--bad)', 
              borderRadius: '0 8px 8px 0',
              fontSize: 13,
              color: 'var(--bad)',
              marginTop: 8,
            }}>
              ⚠️ {error}
            </div>
          )}
        </>
      ) : (
        <div style={{ marginTop: 8 }}>
          <div style={{ 
            padding: '12px 16px', 
            background: 'rgba(72, 187, 120, 0.08)', 
            borderLeft: '4px solid var(--ok)',
            borderRadius: '0 8px 8px 0',
            marginBottom: 12,
          }}>
            <span style={{ color: 'var(--ok)', fontWeight: 'bold', fontSize: 14 }}>
              ✓ Files uploaded successfully
            </span>
          </div>
          <ul style={{ margin: '8px 0 0 0', paddingLeft: 20, fontSize: 13, color: 'var(--muted)' }}>
            <li>📊 <strong>Consumer List:</strong> {uploadedFiles.consumer_list}</li>
            <li>📐 <strong>SLD PDF:</strong> {uploadedFiles.sld_pdf}</li>
          </ul>
          <button 
            onClick={handleReset}
            style={{
              marginTop: 12,
              background: 'none',
              border: '1px solid rgba(255,255,255,0.15)',
              color: 'var(--muted)',
              padding: '6px 14px',
              borderRadius: 6,
              cursor: 'pointer',
              fontSize: 12,
            }}
          >
            ↻ Upload different files
          </button>
        </div>
      )}
    </div>
  );
}
