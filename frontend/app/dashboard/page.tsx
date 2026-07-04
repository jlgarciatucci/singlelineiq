'use client';

import { useState } from 'react';
import { analyzeSession, API_BASE } from '../../components/api';
import SummaryKpis from '../../components/SummaryKpis';
import IssueCard from '../../components/IssueCard';
import TopologyTree from '../../components/TopologyTree';
import SldViewer from '../../components/SldViewer';
import SldReviewPanel from '../../components/SldReviewPanel';
import ReportViewer from '../../components/ReportViewer';
import UploadPanel from '../../components/UploadPanel';

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [uploadedFilenames, setUploadedFilenames] = useState<{ consumer_list: string; sld_pdf: string } | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'topology' | 'issues' | 'sld' | 'report'>('overview');

  const runAnalysis = (sid: string) => {
    setLoading(true);
    setError(null);
    analyzeSession(sid)
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Analysis execution failed.');
        setLoading(false);
      });
  };

  const handleUploadSuccess = (sid: string, filenames: { consumer_list: string; sld_pdf: string }) => {
    setSessionId(sid);
    setUploadedFilenames(filenames);
    runAnalysis(sid);
  };

  const handleRerun = () => {
    if (sessionId) {
      runAnalysis(sessionId);
    }
  };

  const issues = data ? [...data.deterministic_issues, ...data.sld_cross_check_issues] : [];
  const topLoads = data 
    ? [...data.nodes]
        .filter((n: any) => n.asset_role === 'ELECTRICAL_ASSET' && n.downstream_load_kw > 0)
        .sort((a: any, b: any) => b.downstream_load_kw - a.downstream_load_kw)
        .slice(0, 10)
    : [];

  const csvUrl = sessionId 
    ? `${API_BASE}/api/report/issues.csv?session_id=${sessionId}` 
    : `${API_BASE}/api/report/issues.csv`;

  return (
    <main className="container">
      {/* Header Banner Image (Scaled Widescreen) */}
      <div style={{ 
        marginBottom: 20, 
        borderRadius: 12, 
        overflow: 'hidden', 
        border: '1px solid rgba(255,255,255,0.12)', 
        boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
        background: '#07111f',
        maxWidth: '640px',
        margin: '0 auto 20px auto'
      }}>
        <img 
          src="/banner.png" 
          alt="SingleLineIQ - Agentic Electrical Single-Line Reviewer" 
          style={{ width: '100%', height: 'auto', display: 'block' }} 
        />
      </div>

      {/* Control Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>Verification Dashboard</h1>
        </div>
        {sessionId && (
          <div>
            <button 
              onClick={handleRerun} 
              disabled={loading}
              className="button"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1,
                transition: 'all 0.15s ease',
                boxShadow: '0 4px 12px rgba(45, 212, 255, 0.2)'
              }}
            >
              {loading ? (
                <>
                  <span className="spinner" style={{
                    display: 'inline-block',
                    width: 16,
                    height: 16,
                    border: '2px solid rgba(0, 17, 26, 0.3)',
                    borderTopColor: '#00111a',
                    borderRadius: '50%',
                    animation: 'spin 0.8s linear infinite'
                  }} />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <span>⚡</span>
                  <span>Re-run Analysis</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>

      {/* Upload Zone */}
      <div style={{ marginBottom: 24 }}>
        <UploadPanel onUploadSuccess={handleUploadSuccess} />
      </div>

      {/* Show results only after upload + analysis */}
      {!sessionId && !loading && (
        <div className="card" style={{ 
          textAlign: 'center', 
          padding: '60px 20px',
          borderStyle: 'dashed',
          borderColor: 'rgba(45, 212, 255, 0.2)',
        }}>
          <div style={{ fontSize: 48, marginBottom: 16, opacity: 0.5 }}>📤</div>
          <h2 style={{ color: 'var(--muted)', fontWeight: 500 }}>Upload files to begin</h2>
          <p className="muted" style={{ fontSize: 14, maxWidth: 400, margin: '0 auto' }}>
            Drop your Consumer List (CSV/XLSX) and Single-Line Diagram (PDF) in the upload zone above to start the verification pipeline.
          </p>
        </div>
      )}

      {sessionId && (
        <>
          {/* Uploaded files info */}
          {uploadedFilenames && (
            <div className="card" style={{ borderLeft: '4px solid var(--accent)', background: 'rgba(45, 212, 255, 0.05)', marginBottom: 24 }}>
              <p style={{ margin: 0, fontSize: 14 }}>
                📋 <strong>Analyzing:</strong>{' '}
                <code style={{ fontSize: 12 }}>{uploadedFilenames.consumer_list}</code> + <code style={{ fontSize: 12 }}>{uploadedFilenames.sld_pdf}</code>
              </p>
            </div>
          )}

          {/* Quick Stats */}
          {data && (
            <div style={{ marginBottom: 24 }}>
              <SummaryKpis kpis={data.kpis} />
            </div>
          )}

          {/* Tabs Menu */}
          <div style={{
            display: 'flex',
            borderBottom: '1px solid rgba(255,255,255,0.1)',
            marginBottom: 24,
            gap: 16,
            overflowX: 'auto',
            paddingBottom: 4
          }}>
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'topology', label: 'Inferred Network' },
              { id: 'issues', label: `Issues (${issues.length})` },
              { id: 'sld', label: 'SLD Visual Verification' },
              { id: 'report', label: 'Engineering Report' }
            ].map(t => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id as any)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: activeTab === t.id ? 'var(--accent)' : 'var(--muted)',
                  fontSize: 15,
                  fontWeight: 600,
                  padding: '8px 4px',
                  cursor: 'pointer',
                  borderBottom: activeTab === t.id ? '2px solid var(--accent)' : '2px solid transparent',
                  transition: 'all 0.15s ease',
                  whiteSpace: 'nowrap'
                }}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* Tab Panels */}
          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px 0' }}>
              <div className="spinner" style={{
                display: 'inline-block',
                width: 40,
                height: 40,
                border: '3px solid rgba(45, 212, 255, 0.1)',
                borderTopColor: 'var(--accent)',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                marginBottom: 16
              }} />
              <p className="muted">Running electrical network verification engine...</p>
            </div>
          ) : error ? (
            <div className="card critical" style={{ borderLeft: '4px solid var(--bad)', padding: 20 }}>
              <h3>Verification Engine Error</h3>
              <p className="muted">{error}</p>
              <button onClick={handleRerun} className="button" style={{ marginTop: 12 }}>Retry Analysis</button>
            </div>
          ) : data ? (
            <div>
              {activeTab === 'overview' && (
                <div className="grid grid2" style={{ alignItems: 'start' }}>
                  {/* Top Loaded Assets */}
                  <div className="card">
                    <h2>Top Loaded Assets</h2>
                    <p className="muted" style={{ fontSize: 13, marginTop: -4, marginBottom: 12 }}>
                      Electrical boards sorted by downstream loads recursively aggregated.
                    </p>
                    <table>
                      <thead>
                        <tr>
                          <th>Asset Tag</th>
                          <th>Equipment Type</th>
                          <th>Downstream Load</th>
                          <th>Utilization %</th>
                        </tr>
                      </thead>
                      <tbody>
                        {topLoads.map((n: any) => (
                          <tr key={n.node_id}>
                            <td><code>{n.node_id}</code></td>
                            <td><span className="badge" style={{ padding: '2px 8px', fontSize: 11 }}>{n.equipment_type}</span></td>
                            <td>{n.downstream_load_kw.toFixed(1)} kW</td>
                            <td>
                              <span style={{ 
                                color: n.utilization_percent >= 100.0 ? 'var(--bad)' : n.utilization_percent >= 80.0 ? 'var(--warn)' : 'var(--text)',
                                fontWeight: 'bold'
                              }}>
                                {n.utilization_percent ? `${n.utilization_percent.toFixed(1)}%` : '-'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Quick Issue Summary */}
                  <div className="card">
                    <h2>Priority Findings Checklist</h2>
                    <p className="muted" style={{ fontSize: 13, marginTop: -4, marginBottom: 12 }}>
                      Summary of unresolved design inconsistencies and visual mismatches.
                    </p>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                      {issues.slice(0, 5).map((i: any) => (
                        <div key={i.issue_id} style={{
                          padding: 10,
                          background: 'rgba(255,255,255,0.03)',
                          borderRadius: 8,
                          borderLeft: `4px solid ${
                            i.severity === 'critical' ? 'var(--bad)' : i.severity === 'high' ? '#f97316' : 'var(--warn)'
                          }`
                        }}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 2 }}>
                            <strong>{i.issue_id}</strong>
                            <span className="muted">{i.source}</span>
                          </div>
                          <div style={{ fontSize: 13, fontWeight: 600 }}>{i.title}</div>
                          {i.item_tag && <div style={{ fontSize: 11, color: 'var(--accent)', marginTop: 2 }}>Asset: {i.item_tag}</div>}
                        </div>
                      ))}
                      {issues.length > 5 && (
                        <button 
                          onClick={() => setActiveTab('issues')}
                          style={{ background: 'none', border: 'none', color: 'var(--accent)', cursor: 'pointer', textAlign: 'left', fontWeight: 'bold', fontSize: 13, padding: 0 }}
                        >
                          View all {issues.length} issues →
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'topology' && (
                <div className="grid">
                  <TopologyTree nodes={data.nodes} edges={data.edges} />
                </div>
              )}

              {activeTab === 'issues' && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                    <h2>Findings Database</h2>
                    <a href={csvUrl} className="button" style={{ padding: '8px 14px', fontSize: 13, textDecoration: 'none' }}>
                      📥 Export CSV
                    </a>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {issues.map((i: any) => (
                      <IssueCard issue={i} key={i.issue_id} />
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'sld' && (
                <div className="grid grid2" style={{ alignItems: 'start' }}>
                  <SldViewer sessionId={sessionId || undefined} />
                  <SldReviewPanel sldAssets={data.sld_assets} />
                </div>
              )}

              {activeTab === 'report' && (
                <div className="grid">
                  <ReportViewer sessionId={sessionId || undefined} />
                </div>
              )}
            </div>
          ) : null}
        </>
      )}

      <style jsx global>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </main>
  );
}
