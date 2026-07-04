from __future__ import annotations
from fpdf import FPDF
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


class EnrichedReportPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            try:
                # Insert the widescreen logo banner at the top of the cover page
                banner_path = "C:/Users/Jose Luis/.gemini/antigravity-ide/brain/7a4a7582-9a48-420b-a4fd-a2d1c9fbb41a/media__1783174783380.png"
                self.image(banner_path, x=10, y=10, w=190)
                self.set_y(52)
            except Exception:
                self.set_font("helvetica", "B", 16)
                self.cell(0, 10, "SingleLineIQ - Engineering Review Report", align="C")
                self.ln(10)
        else:
            # Sleek small header on subsequent pages
            self.set_font("helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 5, "SingleLineIQ - Engineering Review Report", align="R")
            self.ln(5)
            self.line(10, 15, 200, 15)
            self.set_y(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | SingleLineIQ Automated Verification Review", align="C")


def generate_enriched_pdf_report(
    kpis: dict,
    nodes: list[TopologyNode],
    deterministic: list[ValidationIssue],
    sld_issues: list[ValidationIssue],
    explanations: list[dict],
    input_filenames: dict | None = None,
    is_demo: bool = False
) -> bytes:
    pdf = EnrichedReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. Executive Summary
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(7, 17, 31)  # Dark navy
    pdf.cell(0, 8, "1. Executive Summary")
    pdf.ln(8)
    pdf.ln(1)
    
    # Shaded KPI Box
    pdf.set_fill_color(242, 246, 252)
    pdf.rect(10, pdf.get_y(), 190, 26, style="F")
    
    pdf.set_font("helvetica", "", 9)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(5)
    pdf.cell(90, 6, f"Total Connected Load: {kpis.get('total_connected_load_kw', 0.0):.1f} kW")
    pdf.cell(90, 6, f"Electrical Assets: {kpis.get('electrical_assets', 0)}")
    pdf.ln(6)
    pdf.cell(5)
    pdf.cell(90, 6, f"Final Loads: {kpis.get('final_loads', 0)}")
    pdf.cell(90, 6, f"Network Nodes: {kpis.get('nodes', 0)}")
    pdf.ln(6)
    pdf.cell(5)
    pdf.cell(90, 6, f"Deterministic Issues: {len(deterministic)}")
    pdf.cell(90, 6, f"SLD Cross-check Issues: {len(sld_issues)}")
    pdf.ln(6)
    pdf.ln(6)
    
    # Disclaimer Text
    disclaimer = DISCLAIMER_DEMO if is_demo else DISCLAIMER_USER
    pdf.set_font("helvetica", "I", 9)
    pdf.set_text_color(180, 50, 50)
    pdf.multi_cell(0, 5, disclaimer)
    pdf.ln(4)
    
    # 2. Connected Load Distribution
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(7, 17, 31)
    pdf.cell(0, 8, "2. Connected Load Distribution by Transformer/Switchboard")
    pdf.ln(8)
    pdf.ln(1)
    
    pdf.set_font("helvetica", "B", 8)
    pdf.set_fill_color(225, 235, 248)
    # Table headers
    pdf.cell(70, 5, "Asset Tag", border=1, fill=True)
    pdf.cell(30, 5, "Equipment Type", border=1, fill=True)
    pdf.cell(25, 5, "Capacity (kW)", border=1, fill=True)
    pdf.cell(35, 5, "Aggregated Load (kW)", border=1, fill=True)
    pdf.cell(30, 5, "Utilization (%)", border=1, fill=True)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 8)
    pdf.set_text_color(50, 50, 50)
    distribution_nodes = [n for n in nodes if n.asset_role == "ELECTRICAL_ASSET" and n.downstream_load_kw > 0]
    distribution_nodes = sorted(distribution_nodes, key=lambda n: n.downstream_load_kw, reverse=True)[:12]
    
    for n in distribution_nodes:
        pdf.cell(70, 5, n.node_id, border=1)
        pdf.cell(30, 5, n.equipment_type or "", border=1)
        pdf.cell(25, 5, f"{n.capacity_kw or 0.0:.1f}", border=1)
        pdf.cell(35, 5, f"{n.downstream_load_kw:.1f}", border=1)
        pdf.cell(30, 5, f"{n.utilization_percent or 0.0:.1f}%", border=1)
        pdf.ln(5)
    pdf.ln(6)
    
    # 3. Agent Findings Summarization & Action Plan
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(7, 17, 31)
    pdf.cell(0, 8, "3. Agent Findings Summarization & Action Plan")
    pdf.ln(8)
    pdf.ln(1)
    
    exp_map = {e["issue_id"]: e for e in explanations}
    all_issues = deterministic + sld_issues
    
    if not all_issues:
        pdf.set_font("helvetica", "I", 9)
        pdf.cell(0, 5, "No design validation or drawing consistency issues detected.")
        pdf.ln(5)
    else:
        for issue in all_issues:
            # Header color based on severity
            if issue.severity == "critical":
                pdf.set_text_color(180, 20, 20)
            elif issue.severity == "high":
                pdf.set_text_color(220, 100, 0)
            else:
                pdf.set_text_color(150, 120, 0)
                
            pdf.set_font("helvetica", "B", 9)
            pdf.set_x(10)
            pdf.multi_cell(0, 5, f"Finding {issue.issue_id}: {issue.title} ({issue.severity.upper()})")
            pdf.set_text_color(40, 40, 40)
            
            pdf.set_font("helvetica", "", 8.5)
            if issue.item_tag:
                pdf.set_x(10)
                pdf.cell(0, 4, f"Affected Equipment: {issue.item_tag}")
                pdf.ln(4)
                
            exp_data = exp_map.get(issue.issue_id)
            if exp_data:
                # Double-checking space to avoid orphaned items near page breaks
                if pdf.y > 250:
                    pdf.add_page()
                
                # Render explanations
                pdf.set_font("helvetica", "B", 8)
                pdf.set_x(10)
                pdf.cell(0, 4, "Explanation:")
                pdf.ln(4)
                pdf.set_font("helvetica", "", 8.5)
                pdf.multi_cell(0, 4.2, exp_data["explanation"])
                
                pdf.set_font("helvetica", "B", 8)
                pdf.set_x(10)
                pdf.cell(0, 4, "Likely Impact:")
                pdf.ln(4)
                pdf.set_font("helvetica", "", 8.5)
                pdf.multi_cell(0, 4.2, exp_data["likely_impact"])
                
                pdf.set_font("helvetica", "B", 8)
                pdf.set_x(10)
                pdf.cell(0, 4, "Action Required:")
                pdf.ln(4)
                pdf.set_font("helvetica", "", 8.5)
                pdf.multi_cell(0, 4.2, exp_data["recommended_action"])
                
                pdf.set_font("helvetica", "B", 8)
                pdf.set_x(10)
                pdf.cell(0, 4, "Confidence:")
                pdf.ln(4)
                pdf.set_font("helvetica", "I", 8.5)
                pdf.multi_cell(0, 4.2, exp_data["confidence_note"])
            else:
                pdf.set_font("helvetica", "B", 8)
                pdf.set_x(10)
                pdf.cell(0, 4, "Recommendation:")
                pdf.ln(4)
                pdf.set_font("helvetica", "", 8.5)
                pdf.multi_cell(0, 4.2, issue.recommendation)
            pdf.ln(2.5)
            
    pdf.ln(3)
    
    # 4. Limitations
    if pdf.y > 240:
        pdf.add_page()
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(7, 17, 31)
    pdf.cell(0, 8, "4. Verification Limitations & Boundary Notes")
    pdf.ln(8)
    pdf.ln(1)
    pdf.set_font("helvetica", "", 8.5)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4.5, LIMITATIONS)
    
    return bytes(pdf.output())
