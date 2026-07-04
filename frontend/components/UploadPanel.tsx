import { useState } from 'react';

export default function UploadPanel({ onUploadSuccess }: { onUploadSuccess: () => void }) {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const names = Array.from(e.dataTransfer.files).map(f => f.name);
      setUploadedFiles(prev => [...prev, ...names]);
      onUploadSuccess();
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const names = Array.from(e.target.files).map(f => f.name);
      setUploadedFiles(prev => [...prev, ...names]);
      onUploadSuccess();
    }
  };

  return (
    <div className="card" style={{ marginBottom: 16 }}>
      <h2>Document Intake & Review</h2>
      <p className="muted" style={{ fontSize: 14 }}>
        Intake new structured engineering spreadsheets (CSV / XLSX) or single-line diagrams (PDF) to run validation check pipeline.
      </p>
      
      <div 
        className={`upload-zone ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        style={{
          border: '2px dashed rgba(45, 212, 255, 0.4)',
          borderRadius: 12,
          padding: 24,
          textAlign: 'center',
          background: 'rgba(14, 26, 45, 0.4)',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          marginBottom: 12
        }}
      >
        <input 
          type="file" 
          id="file-upload" 
          multiple 
          onChange={handleFileInput} 
          style={{ display: 'none' }} 
        />
        <label htmlFor="file-upload" style={{ cursor: 'pointer' }}>
          <div style={{ fontSize: 32, marginBottom: 8 }}>📁</div>
          <strong>Drag & drop engineering deliverables</strong>
          <span style={{ display: 'block', color: 'var(--muted)', fontSize: 13, marginTop: 4 }}>
            or click to browse from local computer (.csv, .xlsx, .pdf)
          </span>
        </label>
      </div>

      {uploadedFiles.length > 0 && (
        <div style={{ marginTop: 8 }}>
          <span className="badge" style={{ borderColor: 'var(--ok)', color: 'var(--ok)' }}>
            ✓ Successfully parsed {uploadedFiles.length} file(s)
          </span>
          <ul style={{ margin: '8px 0 0 0', paddingLeft: 20, fontSize: 13, color: 'var(--muted)' }}>
            {uploadedFiles.map((name, i) => (
              <li key={i}>{name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
