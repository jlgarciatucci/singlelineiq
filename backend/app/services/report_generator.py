from __future__ import annotations
from app.schemas import TopologyNode, ValidationIssue

DISCLAIMER_DEMO = (
    "This report was generated from synthetic anonymized data for demonstration purposes only. "
    "It is not based on a real plant, project, client, or confidential engineering deliverable."
)

DISCLAIMER_USER = (
    "This report was generated from user-provided engineering deliverables. "
    "SingleLineIQ performs automated document consistency review only."
)

LIMITATIONS = (
    "SingleLineIQ performs document consistency review and connected-load aggregation. "
    "It does not perform load flow, short-circuit, protection coordination, motor starting, or arc-flash studies."
)

def generate_markdown_report(
    kpis: dict,
    nodes: list[TopologyNode],
    deterministic: list[ValidationIssue],
    sld_issues: list[ValidationIssue],
    explanations: list[dict] | None = None,
    input_filenames: dict | None = None,
    is_demo: bool = False
) -> str:
    lines = []
    
    # 1. Title
    lines.append("# SingleLineIQ Engineering Review Report")
    lines.append("")
    
    # 2. Disclaimer (conditional)
    disclaimer = DISCLAIMER_DEMO if is_demo else DISCLAIMER_USER
    lines.append(f"> {disclaimer}")
    lines.append("")
    
    # 3. Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"- **Electrical assets detected**: {kpis.get('electrical_assets', 0)}")
    lines.append(f"- **Final loads detected**: {kpis.get('final_loads', 0)}")
    lines.append(f"- **Total connected load**: {kpis.get('total_connected_load_kw', 0.0):.1f} kW")
    lines.append(f"- **Deterministic issues**: {len(deterministic)}")
    lines.append(f"- **SLD cross-check issues**: {len(sld_issues)}")
    lines.append("")
    
    # 4. Input Files Reviewed
    fnames = input_filenames or {}
    consumer_fname = fnames.get("consumer_list", "N/A")
    sld_fname = fnames.get("sld_pdf", "N/A")
    lines.append("## 2. Input Files Reviewed")
    lines.append("")
    lines.append(f"- **Consumer List**: `{consumer_fname}`")
    lines.append(f"- **Single-Line Diagram**: `{sld_fname}`")
    lines.append("")
    
    # 5. Topology Graph Summary
    lines.append("## 3. Topology Graph Summary")
    lines.append("")
    lines.append(f"- **Total network nodes**: {kpis.get('nodes', 0)}")
    lines.append(f"- **Connections (edges)**: {kpis.get('edges', 0)}")
    lines.append(f"- **Root nodes**: {len(kpis.get('roots', [])) if isinstance(kpis.get('roots'), list) else kpis.get('roots', 0)}")
    lines.append(f"- **Missing parent items**: {len(kpis.get('missing_parents', [])) if isinstance(kpis.get('missing_parents'), list) else kpis.get('missing_parents', 0)}")
    lines.append(f"- **Cycle structures**: {len(kpis.get('cycles', [])) if isinstance(kpis.get('cycles'), list) else kpis.get('cycles', 0)}")
    lines.append("")
    
    # 6. Load Summary by Transformer
    lines.append("## 4. Load Summary by Transformer")
    lines.append("")
    transformers = [n for n in nodes if n.equipment_type == "TA"]
    if not transformers:
        lines.append("No transformers detected.")
    else:
        lines.append("| Transformer Tag | Primary Voltage (kV) | Capacity (kW) | Downstream Load (kW) | Utilization (%) | Status |")
        lines.append("|---|---|---|---|---|---|")
        for t in transformers:
            lines.append(
                f"| {t.node_id} | {t.voltage_kv or 0.0:.1f} | {t.capacity_kw or 0.0:.1f} | "
                f"{t.downstream_load_kw:.1f} | {t.utilization_percent or 0.0:.1f}% | {t.status} |"
            )
    lines.append("")
    
    # 7. Load Summary by Switchboard
    lines.append("## 5. Load Summary by Switchboard")
    lines.append("")
    switchboards = [n for n in nodes if n.equipment_type in {"HV", "LV"} and ("SWBD" in n.node_id or "SWG" in n.node_id or "SWGR" in n.node_id)]
    if not switchboards:
        lines.append("No switchboards detected.")
    else:
        lines.append("| Switchboard Tag | Nominal Voltage (kV) | Capacity (kW) | Downstream Load (kW) | Utilization (%) | Status |")
        lines.append("|---|---|---|---|---|---|")
        for s in switchboards:
            lines.append(
                f"| {s.node_id} | {s.voltage_kv or 0.0:.2f} | {s.capacity_kw or 0.0:.1f} | "
                f"{s.downstream_load_kw:.1f} | {s.utilization_percent or 0.0:.1f}% | {s.status} |"
            )
    lines.append("")
    
    # 8. Load Summary by MCC/DB
    lines.append("## 6. Load Summary by MCC/DB")
    lines.append("")
    mccs_dbs = [n for n in nodes if n.equipment_type == "MCC" or (n.equipment_type == "LV" and "DB" in n.node_id)]
    if not mccs_dbs:
        lines.append("No MCCs or Distribution Boards detected.")
    else:
        lines.append("| Panel/MCC Tag | Voltage (kV) | Capacity (kW) | Downstream Load (kW) | Utilization (%) | VSD Share (%) | Status |")
        lines.append("|---|---|---|---|---|---|---|")
        for m in mccs_dbs:
            lines.append(
                f"| {m.node_id} | {m.voltage_kv or 0.0:.2f} | {m.capacity_kw or 0.0:.1f} | "
                f"{m.downstream_load_kw:.1f} | {m.utilization_percent or 0.0:.1f}% | {m.vsd_percent:.1f}% | {m.status} |"
            )
    lines.append("")
    
    # Map issue_id to explanations for findings
    exp_map = {e["issue_id"]: e for e in (explanations or [])}
    all_issues = deterministic + sld_issues
    
    # 9. Deterministic Validation Findings
    lines.append("## 7. Deterministic Validation Findings")
    lines.append("")
    if not deterministic:
        lines.append("No deterministic issues found.")
    else:
        for issue in deterministic:
            lines.append(f"### {issue.issue_id} — {issue.title}")
            lines.append(f"- **Severity**: **{issue.severity}**")
            lines.append(f"- **Type**: `{issue.issue_type}`")
            if issue.item_tag:
                lines.append(f"- **Item**: `{issue.item_tag}`")
            if issue.issue_id in exp_map:
                exp = exp_map[issue.issue_id]
                lines.append(f"- **Explanation**: {exp['explanation']}")
                lines.append(f"- **Likely Impact**: {exp['likely_impact']}")
                lines.append(f"- **Recommended Action**: {exp['recommended_action']}")
                lines.append(f"- **Confidence Note**: {exp['confidence_note']}")
            else:
                lines.append(f"- **Recommendation**: {issue.recommendation}")
            lines.append("")
            
    # 10. SLD Visual Cross-Check Findings
    lines.append("## 8. SLD Visual Cross-Check Findings")
    lines.append("")
    if not sld_issues:
        lines.append("No SLD visual cross-check issues found.")
    else:
        for issue in sld_issues:
            lines.append(f"### {issue.issue_id} — {issue.title}")
            lines.append(f"- **Severity**: **{issue.severity}**")
            lines.append(f"- **Confidence**: **{issue.confidence or 0.0:.2f}**")
            if issue.item_tag:
                lines.append(f"- **Item**: `{issue.item_tag}`")
            if issue.issue_id in exp_map:
                exp = exp_map[issue.issue_id]
                lines.append(f"- **Explanation**: {exp['explanation']}")
                lines.append(f"- **Likely Impact**: {exp['likely_impact']}")
                lines.append(f"- **Recommended Action**: {exp['recommended_action']}")
                lines.append(f"- **Confidence Note**: {exp['confidence_note']}")
            else:
                lines.append(f"- **Recommendation**: {issue.recommendation}")
            lines.append("")
            
    # 11. Engineer Action Table
    lines.append("## 9. Engineer Action Table")
    lines.append("")
    if not all_issues:
        lines.append("No action items required.")
    else:
        lines.append("| Issue ID | Severity | Type | Asset Tag | Recommended Action |")
        lines.append("|---|---|---|---|---|")
        for issue in all_issues:
            rec = issue.recommendation
            if issue.issue_id in exp_map:
                rec = exp_map[issue.issue_id]["recommended_action"]
            lines.append(f"| {issue.issue_id} | {issue.severity.upper()} | {issue.issue_type} | {issue.item_tag or '-'} | {rec} |")
    lines.append("")
    
    # 12. Limitations
    lines.append("## 10. Limitations")
    lines.append("")
    lines.append(LIMITATIONS)
    lines.append("")
    
    # 13. Appendix with Evidence
    lines.append("## 11. Appendix: Evidence Data")
    lines.append("")
    if not all_issues:
        lines.append("No evidence to append.")
    else:
        for issue in all_issues:
            lines.append(f"#### {issue.issue_id} Evidence")
            lines.append("- **Direct Evidence Object**:")
            lines.append("```json")
            lines.append(f"{issue.evidence}")
            lines.append("```")
            lines.append("")
            
    return "\n".join(lines)
