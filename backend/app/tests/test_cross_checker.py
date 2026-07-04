from app import config
from app.services.consumer_parser import parse_consumer_list
from app.services.topology_inference import build_topology
from app.services.load_calculator import calculate_loads
from app.services.sld_vision import load_demo_sld_extract
from app.services.cross_checker import cross_check_sld


def test_cross_checker_runs():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    nodes = calculate_loads(topo)
    sld = load_demo_sld_extract(config.SLD_EXTRACT_FILE)
    issues = cross_check_sld(nodes, sld)
    assert isinstance(issues, list)
    assert len(sld) > 0
    
    # Assert expected visual issues from injected issues CSV are detected
    assert any(i.issue_type == "CONSUMER_ASSET_MISSING_FROM_SLD" and i.item_tag == "KPL2-C30-430-LV03-MCC06" for i in issues)
    assert any(i.issue_type == "SLD_ONLY_ASSET" and i.item_tag == "KPL2-X40-440-LV04-MCC09" for i in issues)
    assert any(i.issue_type == "PARENT_MISMATCH" and i.item_tag == "KPL2-B20-420-LV02-MCC04" for i in issues)
