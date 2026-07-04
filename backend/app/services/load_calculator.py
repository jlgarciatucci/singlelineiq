from __future__ import annotations
from app.schemas import ConsumerItem, TopologyNode


def calculate_loads(topology: dict) -> list[TopologyNode]:
    by_id: dict[str, ConsumerItem] = topology["items_by_id"]
    children: dict[str, list[str]] = topology["children"]
    nodes_by_id: dict[str, TopologyNode] = {node.node_id: node.model_copy() for node in topology["nodes"]}

    memo: dict[str, tuple[float, int, int, float | None, str | None]] = {}

    def dfs(node_id: str) -> tuple[float, int, int, float | None, str | None]:
        if node_id in memo:
            return memo[node_id]
        item = by_id.get(node_id)
        if item is None:
            return (0.0, 0, 0, None, None)
        if item.asset_role == "FINAL_LOAD":
            load = item.rated_power_kw or 0.0
            vsd = 1 if (item.starter_type or "").upper() == "VSD" else 0
            count = 1
            largest = load
            largest_tag = item.item_tag
        else:
            load = 0.0
            vsd = 0
            count = 0
            largest = None
            largest_tag = None
        for child_id in children.get(node_id, []):
            c_load, c_count, c_vsd, c_largest, c_largest_tag = dfs(child_id)
            load += c_load
            count += c_count
            vsd += c_vsd
            if c_largest is not None and (largest is None or c_largest > largest):
                largest = c_largest
                largest_tag = c_largest_tag
        memo[node_id] = (load, count, vsd, largest, largest_tag)
        return memo[node_id]

    for node_id, node in nodes_by_id.items():
        load, count, vsd, largest, largest_tag = dfs(node_id)
        node.downstream_load_kw = round(load, 3)
        node.downstream_final_load_count = count
        node.downstream_vsd_count = vsd
        node.vsd_percent = round((vsd / count) * 100, 2) if count else 0.0
        node.largest_downstream_load_kw = round(largest, 3) if largest is not None else None
        node.largest_downstream_load_tag = largest_tag
        if node.asset_role == "ELECTRICAL_ASSET" and node.capacity_kw and node.capacity_kw > 0:
            node.utilization_percent = round((load / node.capacity_kw) * 100, 2)
            if node.utilization_percent >= 100:
                node.status = "critical"
            elif node.utilization_percent >= 85:
                node.status = "warning"
            else:
                node.status = "normal"
        elif node.asset_role == "FINAL_LOAD":
            node.status = "normal"
        else:
            node.status = "unknown"
    return list(nodes_by_id.values())
