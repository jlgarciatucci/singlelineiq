import Link from 'next/link';
export default function Home() {
  return <main className="container hero">
    <span className="badge">Agentic Electrical Single-Line Reviewer</span>
    <h1 className="title">SingleLineIQ</h1>
    <p className="subtitle">An agentic electrical single-line reviewer that infers topology from a full-hierarchy consumer list and cross-checks it against the SLD PDF.</p>
    <p className="muted">Upload your Consumer List and Single-Line Diagram to run an automated document consistency review.</p>
    <Link className="button" href="/dashboard">Start Review →</Link>
  </main>;
}
