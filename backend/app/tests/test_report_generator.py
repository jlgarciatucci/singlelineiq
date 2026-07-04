from app.main import run_pipeline
from app.services.report_generator import generate_markdown_report
from app.services.pdf_generator import generate_enriched_pdf_report


def test_report_contains_sections():
    r = run_pipeline()
    md = generate_markdown_report(r["kpis"], r["nodes"], r["deterministic_issues"], r["sld_cross_check_issues"])
    
    # Assert presence of all 13 required sections or key elements:
    assert "# SingleLineIQ Engineering Review Report" in md
    assert "This report was generated from synthetic anonymized data for demonstration purposes only." in md
    assert "## 1. Executive Summary" in md
    assert "## 2. Input Files Reviewed" in md
    assert "## 3. Topology Graph Summary" in md
    assert "## 4. Load Summary by Transformer" in md
    assert "## 5. Load Summary by Switchboard" in md
    assert "## 6. Load Summary by MCC/DB" in md
    assert "## 7. Deterministic Validation Findings" in md
    assert "## 8. SLD Visual Cross-Check Findings" in md
    assert "## 9. Engineer Action Table" in md
    assert "## 10. Limitations" in md
    assert "## 11. Appendix: Evidence Data" in md


def test_pdf_report_generates():
    r = run_pipeline()
    from app.agents.reasoning_agent import explain_issues
    all_issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    explanations = explain_issues(all_issues, r["kpis"], r["nodes"])
    
    pdf_bytes = generate_enriched_pdf_report(
        r["kpis"],
        r["nodes"],
        r["deterministic_issues"],
        r["sld_cross_check_issues"],
        explanations
    )
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 0
