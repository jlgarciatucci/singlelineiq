from __future__ import annotations
from app.schemas import TopologyNode, SldAsset, ValidationIssue


def cross_check_sld(nodes: list[TopologyNode], sld_assets: list[SldAsset]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seq = 1
    consumer_assets = {n.node_id: n for n in nodes if n.asset_role == "ELECTRICAL_ASSET"}
    visual_assets = {a.item_tag: a for a in sld_assets}

    def add(severity, issue_type, title, item_tag=None, evidence=None, recommendation="Review SLD against consumer list.", confidence=1.0):
        nonlocal seq
        issues.append(ValidationIssue(
            issue_id=f"SLD-{seq:03d}", severity=severity, issue_type=issue_type, title=title,
            item_tag=item_tag, evidence=evidence or {}, recommendation=recommendation,
            source="sld_visual_cross_check", confidence=confidence
        ))
        seq += 1

    # Avoid overflagging upstream assets if visual extraction is partial; focus on panel/switchgear assets.
    relevant_types = {"MCC", "LV", "HV", "TA", "UG"}
    for tag, node in consumer_assets.items():
        if tag not in visual_assets:
            # In demo, MCC06 is intentionally missing. Upstream extraction may be imperfect, so set medium.
            severity = "high" if ("MCC" in tag or "SWBD" in tag or "SWG" in tag) else "medium"
            add(severity, "CONSUMER_ASSET_MISSING_FROM_SLD", f"Consumer-list asset not visible in SLD: {tag}", item_tag=tag,
                evidence={"consumer_parent": node.parent_id, "equipment_type": node.equipment_type},
                recommendation="Verify whether this asset is missing from the single-line diagram or uses a different tag.")

    for tag, asset in visual_assets.items():
        if tag not in consumer_assets:
            add("medium", "SLD_ONLY_ASSET", f"SLD-only asset not found in consumer list: {tag}", item_tag=tag,
                evidence={"visual_parent": asset.parent_tag, "asset_type": asset.asset_type},
                recommendation="Verify whether this is a spare, future feeder, or missing consumer-list row.", confidence=asset.confidence)

    for tag, visual in visual_assets.items():
        if tag in consumer_assets and visual.parent_tag:
            consumer_parent = consumer_assets[tag].parent_id
            if consumer_parent and visual.parent_tag != consumer_parent:
                add("high", "PARENT_MISMATCH", f"Parent mismatch for {tag}", item_tag=tag,
                    evidence={"consumer_parent": consumer_parent, "sld_parent": visual.parent_tag},
                    recommendation="Resolve parent assignment between consumer list and SLD drawing.", confidence=visual.confidence)
        if tag in consumer_assets:
            node = consumer_assets[tag]
            if visual.capacity_kw is not None and node.capacity_kw is not None:
                diff = abs(visual.capacity_kw - node.capacity_kw)
                if diff > max(1.0, 0.05 * node.capacity_kw):
                    add("medium", "CAPACITY_MISMATCH", f"Capacity mismatch for {tag}", item_tag=tag,
                        evidence={"consumer_capacity_kw": node.capacity_kw, "sld_capacity_kw": visual.capacity_kw, "difference_kw": diff},
                        recommendation="Confirm whether the SLD rating or consumer-list capacity is current.", confidence=visual.confidence)
            if visual.voltage_kv is not None and node.voltage_kv is not None:
                if visual.voltage_kv != node.voltage_kv:
                    add("high", "VOLTAGE_MISMATCH", f"Voltage mismatch for {tag} between consumer list and visual SLD", item_tag=tag,
                        evidence={"consumer_voltage_kv": node.voltage_kv, "sld_voltage_kv": visual.voltage_kv},
                        recommendation="Confirm correct voltage rating from design data sheet.", confidence=visual.confidence)
            if visual.confidence < 0.8:
                add("low", "LOW_CONFIDENCE_EXTRACTION", f"Low confidence visual extraction for {tag}", item_tag=tag,
                    evidence={"visual_confidence": visual.confidence},
                    recommendation="Manually inspect this asset on the single-line diagram to confirm.", confidence=visual.confidence)
    return issues
