import { useState } from 'react';

export default function SldReviewPanel({ sldAssets }: { sldAssets: any[] }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = (sldAssets || []).filter(a => 
    a.item_tag.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (a.notes && a.notes.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, flexWrap: 'wrap', gap: 8 }}>
        <h2>SLD Visual Extraction Details</h2>
        <input 
          type="text" 
          placeholder="Search extracted assets..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            background: 'var(--bg)',
            color: 'var(--text)',
            border: '1px solid rgba(255,255,255,0.12)',
            borderRadius: 8,
            padding: '6px 12px',
            fontSize: 13
          }}
        />
      </div>
      <p className="muted" style={{ fontSize: 13, marginTop: -4, marginBottom: 12 }}>
        These electrical assets were extracted visually from `SingleLineDiagram.pdf` by the vision system/Gemini model.
      </p>
      
      <div style={{ overflowX: 'auto', maxHeight: 400, overflowY: 'auto' }}>
        <table>
          <thead>
            <tr>
              <th>Asset Tag</th>
              <th>Type</th>
              <th>Voltage</th>
              <th>Capacity</th>
              <th>Parent Tag</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} className="muted" style={{ textAlign: 'center' }}>No extracted assets found.</td></tr>
            ) : (
              filtered.map((a: any) => (
                <tr key={a.item_tag}>
                  <td><code>{a.item_tag}</code></td>
                  <td><span className="badge" style={{ padding: '2px 8px', fontSize: 11 }}>{a.asset_type}</span></td>
                  <td>{a.voltage_kv !== null ? `${a.voltage_kv} kV` : '-'}</td>
                  <td>{a.capacity_kw !== null ? `${a.capacity_kw.toFixed(1)} kW` : '-'}</td>
                  <td>{a.parent_tag ? <code>{a.parent_tag}</code> : <span className="muted">None (Root)</span>}</td>
                  <td>
                    <span style={{ 
                      color: a.confidence >= 0.9 ? 'var(--ok)' : a.confidence >= 0.7 ? 'var(--warn)' : 'var(--bad)',
                      fontWeight: 'bold'
                    }}>
                      {(a.confidence * 100).toFixed(0)}%
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
