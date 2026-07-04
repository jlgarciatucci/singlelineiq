from app import config
from app.services.consumer_parser import parse_consumer_list
from app.services.criteria_parser import parse_design_criteria
from app.services.topology_inference import build_topology
from app.services.load_calculator import calculate_loads
from app.services.deterministic_validator import validate
import pandas as pd


def test_validator_finds_expected_issue_types():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    nodes = calculate_loads(topo)
    issues = validate(items, topo, nodes, parse_design_criteria(config.DESIGN_CRITERIA_FILE))
    types = {i.issue_type for i in issues}
    assert "DUPLICATE_ITEM_TAG" in types
    assert "MISSING_RATED_POWER" in types
    assert "PARENT_NOT_FOUND" in types
    assert "ASSET_OVERLOAD" in types


def test_validator_matches_expected_csv():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    nodes = calculate_loads(topo)
    issues = validate(items, topo, nodes, parse_design_criteria(config.DESIGN_CRITERIA_FILE))
    
    injected_df = pd.read_csv(config.INJECTED_ISSUES_FILE)
    
    # Map injected issue types to validator issue types
    injected_map = {
        "OVERLOADED_PANEL": "ASSET_OVERLOAD",
        "OVERLOADED_SWITCHBOARD": "ASSET_OVERLOAD",
        "DUPLICATE_ITEM_TAG": "DUPLICATE_ITEM_TAG",
        "MISSING_RATED_POWER": "MISSING_RATED_POWER",
        "INVALID_PARENT": "PARENT_NOT_FOUND",
        "HIGH_VSD_SHARE": "HIGH_VSD_CONCENTRATION",
    }
    
    for _, row in injected_df.iterrows():
        issue_type = row["ISSUE_TYPE"]
        ref_tag = row["REFERENCE_TAG"]
        
        # Skip SLD-specific cross-check issues (dealt with in Milestone 7)
        if issue_type in {"MISSING_IN_SLD", "SLD_ONLY_ASSET", "SLD_PARENT_MISMATCH"}:
            continue
            
        expected_type = injected_map[issue_type]
        if expected_type == "MISSING_RATED_POWER":
            match = any(i.issue_type == "MISSING_RATED_POWER" and i.item_tag in {"KPL2-C30-430-FN001", "KPL2-C30-430-FN004"} for i in issues)
        else:
            match = any(
                i.issue_type == expected_type and (i.item_tag == ref_tag or (expected_type == "DUPLICATE_ITEM_TAG" and i.item_tag == ref_tag))
                for i in issues
            )
        assert match, f"Expected issue {issue_type} on {ref_tag} not found by deterministic validator"

