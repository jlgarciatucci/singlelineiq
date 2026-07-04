import { useState } from 'react';

export default function IssueCard({ issue }: { issue: any }) {
  const [expanded, setExpanded] = useState(false);

  const severityColor = 
    issue.severity === 'critical' ? 'var(--bad)' : 
    issue.severity === 'high' ? '#f97316' : 
    issue.severity === 'medium' ? 'var(--warn)' : 'var(--ok)';

  return (
    <div style={{
      background: 'rgba(14, 26, 45, 0.6)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: 10,
      marginBottom: 8,
      overflow: 'hidden',
      width: '100%',
      transition: 'all 0.2s ease'
    }}>
      {/* Header Row */}
      <div 
        onClick={() => setExpanded(!expanded)}
        style={{
          padding: '12px 16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          cursor: 'pointer',
          borderLeft: `4px solid ${severityColor}`,
          userSelect: 'none'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
          <span style={{ fontSize: 11, fontWeight: 'bold', background: 'rgba(255,255,255,0.08)', padding: '2px 6px', borderRadius: 4, color: 'var(--muted)' }}>
            {issue.issue_id}
          </span>
          <span className="badge" style={{ 
            borderColor: severityColor, 
            color: severityColor,
            fontSize: 10,
            padding: '1px 6px'
          }}>
            {issue.severity.toUpperCase()}
          </span>
          <span style={{ fontWeight: 600, fontSize: 14 }}>{issue.title}</span>
          {issue.item_tag && (
            <code style={{ fontSize: 12, color: 'var(--accent)', background: 'rgba(45, 212, 255, 0.05)', padding: '2px 6px', borderRadius: 4 }}>
              {issue.item_tag}
            </code>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 12, color: 'var(--muted)' }}>{issue.source}</span>
          <span style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s ease', fontSize: 10 }}>▼</span>
        </div>
      </div>

      {/* Expanded Content Area */}
      {expanded && (
        <div style={{ padding: '16px 20px', background: 'rgba(7, 17, 31, 0.4)', borderTop: '1px solid rgba(255,255,255,0.06)' }}>
          <p style={{ margin: '0 0 12px 0', fontSize: 14, lineHeight: 1.4 }}>
            <strong>Recommendation:</strong> {issue.recommendation}
          </p>
          <div style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 12 }}>
            <strong>Check Type:</strong> <code>{issue.issue_type}</code>
          </div>
          {issue.evidence && Object.keys(issue.evidence).length > 0 && (
            <div>
              <div style={{ fontSize: 12, fontWeight: 'bold', color: 'var(--muted)', marginBottom: 6 }}>Evidence Context:</div>
              <pre style={{ margin: 0, padding: 12, background: 'rgba(0,0,0,0.3)', borderRadius: 6, fontSize: 11, border: 'none' }}>
                {JSON.stringify(issue.evidence, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
