from __future__ import annotations
from collections import Counter
from app.schemas import ConsumerItem, TopologyNode, ValidationIssue


def validate(items: list[ConsumerItem], topology: dict, nodes: list[TopologyNode], criteria: dict | None = None) -> list[ValidationIssue]:
    criteria = criteria or {}
    warning_pct = float(criteria.get("asset_overload_warning_percent", 85.0))
    critical_pct = float(criteria.get("asset_overload_critical_percent", 100.0))
    high_vsd_pct = float(criteria.get("high_vsd_concentration_percent", 70.0))
    issues: list[ValidationIssue] = []
    seq = 1

    def add(severity, issue_type, title, item_tag=None, parent_tag=None, evidence=None, recommendation="Review with responsible electrical engineer."):
        nonlocal seq
        issues.append(ValidationIssue(
            issue_id=f"DET-{seq:03d}",
            severity=severity,
            issue_type=issue_type,
            title=title,
            item_tag=item_tag,
            parent_tag=parent_tag,
            evidence=evidence or {},
            recommendation=recommendation,
            source="deterministic_calculation",
            confidence=1.0,
        ))
        seq += 1

    counts = Counter(i.item_tag for i in items)
    for tag, count in counts.items():
        if count > 1:
            add("high", "DUPLICATE_ITEM_TAG", f"Duplicate ITEM TAG detected: {tag}", item_tag=tag,
                evidence={"count": count}, recommendation="Keep a unique ITEM TAG per asset/load or confirm intentional duplicate handling.")

    by_id = topology["items_by_id"]
    for item in items:
        if item.asset_role == "FINAL_LOAD" and item.rated_power_kw is None:
            add("medium", "MISSING_RATED_POWER", f"Final load has missing RATED POWER: {item.item_tag}", item_tag=item.item_tag,
                parent_tag=item.parent_item_tag, evidence={"item_tag": item.item_tag, "rated_power": None},
                recommendation="Populate RATED POWER before final load aggregation or capacity review.")
        if item.item_tag not in topology.get("roots", []) and not item.parent_item_tag:
            add("high", "MISSING_PARENT_ITEM_TAG", f"Non-root item has no PARENT ITEM TAG: {item.item_tag}", item_tag=item.item_tag,
                evidence={"asset_role": item.asset_role}, recommendation="Assign a valid PARENT ITEM TAG.")
        if item.parent_item_tag and item.parent_item_tag not in by_id:
            add("critical", "PARENT_NOT_FOUND", f"Parent item tag not found for {item.item_tag}", item_tag=item.item_tag,
                parent_tag=item.parent_item_tag, evidence={"missing_parent": item.parent_item_tag},
                recommendation="Correct the parent hierarchy or add the missing upstream asset row.")

    for cycle in topology.get("cycles", []):
        add("critical", "TOPOLOGY_CYCLE", "Cycle detected in electrical hierarchy", evidence={"cycle": cycle},
            recommendation="Break the circular parent-child relationship.")

    node_map = {n.node_id: n for n in nodes}
    for node in nodes:
        if node.asset_role == "ELECTRICAL_ASSET" and node.utilization_percent is not None:
            if node.utilization_percent >= critical_pct:
                add("critical", "ASSET_OVERLOAD", f"{node.node_id} exceeds capacity", item_tag=node.node_id,
                    evidence={"capacity_kw": node.capacity_kw, "downstream_load_kw": node.downstream_load_kw, "utilization_percent": node.utilization_percent},
                    recommendation="Review load allocation, capacity rating, or design criteria.")
            elif node.utilization_percent >= warning_pct:
                add("medium", "HIGH_ASSET_LOADING", f"{node.node_id} is highly loaded", item_tag=node.node_id,
                    evidence={"capacity_kw": node.capacity_kw, "downstream_load_kw": node.downstream_load_kw, "utilization_percent": node.utilization_percent},
                    recommendation="Verify spare capacity and future load allowance.")
        if node.equipment_type == "MCC" and node.downstream_final_load_count >= 3 and node.vsd_percent >= high_vsd_pct:
            add("medium", "HIGH_VSD_CONCENTRATION", f"High VSD concentration on {node.node_id}", item_tag=node.node_id,
                evidence={"vsd_percent": node.vsd_percent, "vsd_count": node.downstream_vsd_count, "load_count": node.downstream_final_load_count},
                recommendation="Review harmonic/filtering assumptions and VSD grouping.")

    # Basic invalid hierarchy: final load cannot have children
    children = topology.get("children", {})
    for item in items:
        if item.asset_role == "FINAL_LOAD" and children.get(item.item_tag):
            add("critical", "INVALID_HIERARCHY", f"Final load has downstream children: {item.item_tag}", item_tag=item.item_tag,
                evidence={"children": children.get(item.item_tag)}, recommendation="Final loads should not feed other assets.")

    # Voltage mismatch check
    for item in items:
        if item.parent_item_tag and item.parent_item_tag in by_id:
            parent_item = by_id[item.parent_item_tag]
            if parent_item.equipment_type != "TA":
                if item.rated_voltage_kv is not None and parent_item.rated_voltage_kv is not None:
                    if item.rated_voltage_kv != parent_item.rated_voltage_kv:
                        add("high", "VOLTAGE_MISMATCH", 
                            f"Voltage mismatch: parent {parent_item.item_tag} is {parent_item.rated_voltage_kv} kV, child {item.item_tag} is {item.rated_voltage_kv} kV",
                            item_tag=item.item_tag, parent_tag=parent_item.item_tag,
                            evidence={"parent_voltage": parent_item.rated_voltage_kv, "child_voltage": item.rated_voltage_kv},
                            recommendation="Ensure the voltage levels of parent and child match or insert a step-down transformer.")

    return issues
