from app import config
from app.services.consumer_parser import parse_consumer_list
from app.services.topology_inference import build_topology
from app.services.load_calculator import calculate_loads


def test_loads_calculate_downstream():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    nodes = calculate_loads(topo)
    mcc = next(n for n in nodes if n.node_id == "KPL2-A10-410-LV01-MCC01")
    assert mcc.downstream_final_load_count > 0
    assert mcc.downstream_load_kw > 0
    assert mcc.utilization_percent is not None
    
    # Assert largest downstream load calculations
    assert mcc.largest_downstream_load_kw == 75.0
    assert mcc.largest_downstream_load_tag == "KPL2-A10-410-PP002"

    # Test handling of missing final-load rating safely
    # A final load with missing rating (None) should use 0.0 without crashing
    bad_item = next(i for i in items if i.asset_role == "FINAL_LOAD" and i.rated_power_kw is None)
    bad_node = next(n for n in nodes if n.node_id == bad_item.item_tag)
    assert bad_node.direct_load_kw == 0.0

