import { useState, useEffect } from 'react';
import { getReport, API_BASE } from './api';

interface ReportViewerProps {
  sessionId?: string;
}

function parseMarkdownToHtml(md: string) {
  const lines = md.split('\n');
  const elements: React.ReactNode[] = [];
  let inTable = false;
  let tableHeaders: string[] = [];
  let tableRows: string[][] = [];
  let inList = false;
  let listItems: React.ReactNode[] = [];

  const flushList = (key: number) => {
    if (inList && listItems.length > 0) {
      elements.push(<ul key={`ul-${key}`} style={{ paddingLeft: 24, marginBottom: 16, listStyleType: 'disc' }}>{listItems}</ul>);
      listItems = [];
      inList = false;
    }
  };

  const flushTable = (key: number) => {
    if (inTable && tableHeaders.length > 0) {
      elements.push(
        <div key={`table-wrapper-${key}`} style={{ overflowX: 'auto', marginBottom: 24, border: '1px solid rgba(255,255,255,0.08)', borderRadius: 8 }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13, background: 'rgba(7, 17, 31, 0.4)' }}>
            <thead>
              <tr style={{ background: 'rgba(45, 212, 255, 0.08)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                {tableHeaders.map((h, i) => (
                  <th key={i} style={{ padding: '10px 14px', textAlign: 'left', fontWeight: 'bold', borderRight: '1px solid rgba(255,255,255,0.06)', color: 'var(--accent)' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableRows.map((row, ri) => (
                <tr key={ri} style={{ borderBottom: '1px solid rgba(255,255,255,0.06)', background: ri % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.02)' }}>
                  {row.map((cell, ci) => (
                    <td key={ci} style={{ padding: '10px 14px', borderRight: '1px solid rgba(255,255,255,0.06)' }}>{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
      tableHeaders = [];
      tableRows = [];
      inTable = false;
    }
  };

  const formatText = (text: string) => {
    const parts = text.split(/\*\*([^*]+)\*\*/g);
    return parts.map((part, index) => {
      if (index % 2 === 1) {
        return <strong key={index} style={{ color: 'var(--accent)' }}>{part}</strong>;
      }
      return part;
    });
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (line === '---' || line === '***') {
      flushList(i);
      flushTable(i);
      elements.push(<hr key={i} style={{ border: 'none', borderBottom: '1px solid rgba(255,255,255,0.08)', margin: '24px 0' }} />);
      continue;
    }

    if (line.startsWith('#')) {
      flushList(i);
      flushTable(i);
      const headingLevel = line.match(/^#+/)?.[0].length || 1;
      const text = line.replace(/^#+\s*/, '');
      const formatted = formatText(text);

      if (headingLevel === 1) {
        elements.push(<h1 key={i} style={{ fontSize: 24, marginTop: 28, marginBottom: 14, borderBottom: '2px solid var(--accent)', paddingBottom: 8, color: '#ffffff' }}>{formatted}</h1>);
      } else if (headingLevel === 2) {
        elements.push(<h2 key={i} style={{ fontSize: 18, marginTop: 22, marginBottom: 12, color: 'var(--accent)', fontWeight: 'bold' }}>{formatted}</h2>);
      } else if (headingLevel === 3) {
        elements.push(<h3 key={i} style={{ fontSize: 15, marginTop: 18, marginBottom: 10, color: '#ffffff' }}>{formatted}</h3>);
      } else {
        elements.push(<h4 key={i} style={{ fontSize: 13, marginTop: 14, marginBottom: 8, fontWeight: 'bold', color: '#ffffff' }}>{formatted}</h4>);
      }
      continue;
    }

    if (line.startsWith('- ') || line.startsWith('* ')) {
      flushTable(i);
      inList = true;
      const text = line.replace(/^[-*]\s+/, '');
      listItems.push(<li key={`li-${i}`} style={{ marginBottom: 8, fontSize: 14, color: 'rgba(255,255,255,0.85)' }}>{formatText(text)}</li>);
      continue;
    }

    if (line.startsWith('|')) {
      flushList(i);
      const cells = line.split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
      
      const isSeparator = cells.every(c => /^:-*|-*:$/g.test(c) || /^-+$/g.test(c));
      if (isSeparator) {
        continue;
      }

      if (!inTable) {
        inTable = true;
        tableHeaders = cells;
      } else {
        tableRows.push(cells);
      }
      continue;
    }

    if (line === '') {
      flushList(i);
      flushTable(i);
      continue;
    }

    if (line.startsWith('>')) {
      flushList(i);
      flushTable(i);
      const text = line.replace(/^>\s*/, '');
      const isDisclaimer = text.includes('demonstration purposes only') || text.includes('synthetic anonymized data');
      elements.push(
        <div key={i} style={{ 
          borderLeft: '4px solid ' + (isDisclaimer ? 'var(--bad)' : 'var(--accent)'), 
          background: isDisclaimer ? 'rgba(255, 100, 100, 0.05)' : 'rgba(45, 212, 255, 0.05)', 
          padding: '12px 16px', 
          borderRadius: '0 8px 8px 0',
          marginBottom: 18,
          fontStyle: 'italic',
          fontSize: 14,
          lineHeight: 1.5,
          color: isDisclaimer ? 'var(--bad)' : 'rgba(255,255,255,0.9)'
        }}>
          {formatText(text)}
        </div>
      );
      continue;
    }

    flushList(i);
    flushTable(i);
    elements.push(<p key={i} style={{ fontSize: 14, lineHeight: 1.6, marginBottom: 16, color: 'rgba(255,255,255,0.85)' }}>{formatText(line)}</p>);
  }

  flushList(lines.length);
  flushTable(lines.length);

  return elements;
}

export default function ReportViewer({ sessionId }: ReportViewerProps) {
  const [report, setReport] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getReport(sessionId)
      .then(text => {
        setReport(text);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Failed to fetch report');
        setLoading(false);
      });
  }, [sessionId]);

  const pdfUrl = sessionId 
    ? `${API_BASE}/api/report/pdf?session_id=${sessionId}` 
    : `${API_BASE}/api/report/pdf`;

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <h2>Engineering Review Report</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <a href={pdfUrl} className="button" style={{ padding: '8px 14px', fontSize: 13, background: 'var(--accent)', color: '#00111a', textDecoration: 'none' }}>
            📄 Download PDF Report
          </a>
        </div>
      </div>
      
      {loading ? (
        <p className="muted">Generating Markdown report...</p>
      ) : error ? (
        <p style={{ color: 'var(--bad)' }}>Error: {error}</p>
      ) : (
        <div style={{
          maxHeight: 600,
          overflowY: 'auto',
          background: 'rgba(7, 17, 31, 0.4)',
          border: '1px solid rgba(255,255,255,0.06)',
          borderRadius: 8,
          padding: '24px 28px',
          boxShadow: 'inset 0 2px 8px rgba(0,0,0,0.2)'
        }}>
          {parseMarkdownToHtml(report)}
        </div>
      )}
    </div>
  );
}
