interface DemoRunButtonProps {
  onRun: () => void;
  loading: boolean;
}

export default function DemoRunButton({ onRun, loading }: DemoRunButtonProps) {
  return (
    <button 
      onClick={onRun} 
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
          <span>Executing Verification Agent...</span>
        </>
      ) : (
        <>
          <span>⚡</span>
          <span>Run SingleLine Diagram Review</span>
        </>
      )}
      <style jsx global>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </button>
  );
}
