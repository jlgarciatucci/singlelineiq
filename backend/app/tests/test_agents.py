from unittest.mock import patch
from app.schemas import ValidationIssue
from app.agents.reasoning_agent import explain_issues
from app.agents.report_review_agent import review_report


def test_explain_issues_fallback():
    mock_issues = [
        ValidationIssue(
            issue_id="DET-001",
            severity="critical",
            issue_type="ASSET_OVERLOAD",
            title="Overload",
            item_tag="KPL2-TEST-PANEL",
            evidence={"capacity_kw": 100.0, "downstream_load_kw": 120.0, "utilization_percent": 120.0},
            recommendation="Mock rec",
            source="deterministic_calculation",
            confidence=1.0
        )
    ]
    
    with patch("app.config.USE_GEMINI", False):
        explanations = explain_issues(mock_issues, {}, [])
        assert len(explanations) == 1
        exp = explanations[0]
        assert exp["issue_id"] == "DET-001"
        assert "exceeds" in exp["explanation"]
        assert "overheating" in exp["likely_impact"]
        assert "redistribute" in exp["recommended_action"]
        assert "Calculated from" in exp["confidence_note"]


def test_explain_issues_gemini_mocked():
    mock_issues = [
        ValidationIssue(
            issue_id="DET-001",
            severity="critical",
            issue_type="ASSET_OVERLOAD",
            title="Overload",
            item_tag="KPL2-TEST-PANEL",
            evidence={"capacity_kw": 100.0, "downstream_load_kw": 120.0, "utilization_percent": 120.0},
            recommendation="Mock rec",
            source="deterministic_calculation",
            confidence=1.0
        )
    ]
    
    mock_gemini_resp = [
        {
            "issue_id": "DET-001",
            "explanation": "Gemini explanation",
            "likely_impact": "Gemini impact",
            "recommended_action": "Gemini action",
            "confidence_note": "Gemini confidence"
        }
    ]
    
    with patch("app.config.USE_GEMINI", True), \
         patch("app.config.GOOGLE_API_KEY", "some_key"), \
         patch("app.agents.reasoning_agent.call_gemini_to_explain", return_value=mock_gemini_resp):
        
        explanations = explain_issues(mock_issues, {}, [])
        assert len(explanations) == 1
        exp = explanations[0]
        assert exp["issue_id"] == "DET-001"
        assert exp["explanation"] == "Gemini explanation"
        assert exp["likely_impact"] == "Gemini impact"
        assert exp["recommended_action"] == "Gemini action"
        assert exp["confidence_note"] == "Gemini confidence"


def test_review_report_fallback():
    report = "# Test Report"
    with patch("app.config.USE_GEMINI", False):
        reviewed = review_report(report)
        assert "reviewed by automated validation boundaries" in reviewed


def test_review_report_gemini_mocked():
    report = "# Test Report"
    mock_reviewed = "# Polished Test Report"
    
    with patch("app.config.USE_GEMINI", True), \
         patch("app.config.GOOGLE_API_KEY", "some_key"), \
         patch("app.agents.report_review_agent.call_gemini_to_review", return_value=mock_reviewed):
         
        reviewed = review_report(report)
        assert reviewed == "# Polished Test Report"
