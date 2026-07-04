from __future__ import annotations
from collections import defaultdict, deque
from app.schemas import ConsumerItem, TopologyEdge, TopologyNode

class TopologyResult(dict):
    pass

def build_topology(items: list[ConsumerItem]) -> dict:
    by_id: dict[str, ConsumerItem] = {}
    duplicates: list[str] = []
    for item in items:
        if item.item_tag in by_id:
            duplicates.append(item.item_tag)
        by_id[item.item_tag] = item

    children: dict[str, list[str]] = defaultdict(list)
    edges: list[TopologyEdge] = []
    missing_parents: list[dict] = []
    roots: list[str] = []

    for item in items:
        parent = item.parent_item_tag
        if parent:
            edges.append(TopologyEdge(parent_id=parent, child_id=item.item_tag))
            children[parent].append(item.item_tag)
            if parent not in by_id:
                missing_parents.append({"item_tag": item.item_tag, "parent_item_tag": parent})
        else:
            roots.append(item.item_tag)

    def path_to_root(node_id: str) -> list[str]:
        path = []
        seen = set()
        current = node_id
        while current and current in by_id and current not in seen:
            seen.add(current)
            path.append(current)
            current = by_id[current].parent_item_tag or ""
        return list(reversed(path))

    nodes = []
    for item in items:
        capacity = item.rated_power_kw if item.asset_role == "ELECTRICAL_ASSET" else None
        direct_load = item.rated_power_kw if item.asset_role == "FINAL_LOAD" and item.rated_power_kw is not None else 0.0
        nodes.append(TopologyNode(
            node_id=item.item_tag,
            parent_id=item.parent_item_tag,
            asset_role=item.asset_role,
            equipment_type=item.equipment_type,
            description=item.description,
            voltage_kv=item.rated_voltage_kv,
            capacity_kw=capacity,
            direct_load_kw=direct_load,
            path=path_to_root(item.item_tag),
        ))

    cycles = detect_cycles(by_id)
    return {
        "items_by_id": by_id,
        "children": dict(children),
        "nodes": nodes,
        "edges": edges,
        "roots": roots,
        "duplicates": duplicates,
        "missing_parents": missing_parents,
        "cycles": cycles,
    }

def detect_cycles(by_id: dict[str, ConsumerItem]) -> list[list[str]]:
    cycles = []
    for start in by_id:
        seen = {}
        current = start
        step = 0
        while current in by_id:
            if current in seen:
                cycle_start = seen[current]
                chain = list(seen.keys())
                cycles.append(chain[cycle_start:])
                break
            seen[current] = step
            step += 1
            parent = by_id[current].parent_item_tag
            if not parent:
                break
            current = parent
    # de-duplicate cycles by sorted key
    out = []
    keys = set()
    for c in cycles:
        k = tuple(sorted(c))
        if k not in keys:
            keys.add(k)
            out.append(c)
    return out
