'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import ReportViewer from '../../components/ReportViewer';
import Link from 'next/link';

function ReportContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('session_id') || undefined;

  return (
    <>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 24 }}>
        <h1>Engineering Analysis Report</h1>
      </div>
      <p style={{ marginBottom: 20 }}>
        <Link href="/dashboard" className="button" style={{ background: 'rgba(255,255,255,0.1)', color: 'var(--text)', textDecoration: 'none', padding: '8px 14px', fontSize: 13, marginRight: 12 }}>
          ← Back to Dashboard
        </Link>
      </p>
      <ReportViewer sessionId={sessionId} />
    </>
  );
}

export default function ReportPage() {
  return (
    <main className="container">
      <Suspense fallback={<p className="muted">Loading report...</p>}>
        <ReportContent />
      </Suspense>
    </main>
  );
}
