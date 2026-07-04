export default function SummaryKpis({ kpis }: { kpis: any }) {
  const items = [
    ['Assets', kpis?.electrical_assets],
    ['Final loads', kpis?.final_loads],
    ['Connected kW', Number(kpis?.total_connected_load_kw || 0).toFixed(1)],
    ['Issues', (kpis?.deterministic_issues || 0) + (kpis?.sld_cross_check_issues || 0)],
  ];
  return <div className="grid grid4">{items.map(([label, value]) => <div className="card" key={label}><div className="muted">{label}</div><div className="kpi">{value}</div></div>)}</div>;
}
