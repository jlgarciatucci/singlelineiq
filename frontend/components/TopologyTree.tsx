function buildTree(nodes: any[], edges: any[]) {
  const byId = new Map(nodes.map((n) => [n.node_id, { ...n, children: [] }]));
  edges.forEach((e) => {
    const parent = byId.get(e.parent_id); const child = byId.get(e.child_id);
    if (parent && child) parent.children.push(child);
  });
  return Array.from(byId.values()).filter((n: any) => !n.parent_id || !byId.has(n.parent_id));
}
function Node({ node, depth = 0 }: { node: any; depth?: number }) {
  const pad = '  '.repeat(depth);
  const label = `${pad}${depth ? '└─ ' : ''}${node.node_id} (${node.equipment_type || node.asset_role}) load=${node.downstream_load_kw} kW`;
  return <>{label}<br />{node.children?.slice(0, 80).map((c: any) => <Node key={c.node_id} node={c} depth={depth + 1} />)}</>;
}
export default function TopologyTree({ nodes, edges }: { nodes: any[]; edges: any[] }) {
  const roots = buildTree(nodes || [], edges || []);
  return <div className="card"><h2>Inferred topology</h2><div className="topology">{roots.map((r: any) => <Node key={r.node_id} node={r} />)}</div></div>;
}
