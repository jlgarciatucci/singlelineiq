from app import config
from app.services.consumer_parser import parse_consumer_list
from app.services.topology_inference import build_topology
import pandas as pd


def test_topology_builds_edges_and_missing_parent():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    assert len(topo["nodes"]) == len(items)
    assert any(e.parent_id == "KPL2-MAIN-3300-SWGR01" and e.child_id == "KPL2-MAIN-3300-TR00" for e in topo["edges"])
    assert topo["missing_parents"]


def test_topology_matches_expected_csv():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    topo = build_topology(items)
    
    expected_df = pd.read_csv(config.EXPECTED_TOPOLOGY_FILE)
    nodes_by_id = {node.node_id: node for node in topo["nodes"]}
    
    for _, row in expected_df.iterrows():
        item_tag = row["ITEM TAG"]
        assert item_tag in nodes_by_id, f"Node {item_tag} missing from topology"
        
        node = nodes_by_id[item_tag]
        
        # Check parent-child relationship
        expected_parent = row["PARENT ITEM TAG"]
        if pd.isna(expected_parent) or expected_parent == "":
            assert node.parent_id is None or node.parent_id == "", f"Node {item_tag} should have no parent, but got {node.parent_id}"
        else:
            assert node.parent_id == expected_parent, f"Node {item_tag} parent mismatch: expected {expected_parent}, got {node.parent_id}"
            
        # Check asset role and equipment type
        assert node.asset_role == row["ASSET ROLE"], f"Node {item_tag} asset role mismatch"
        
        expected_eq_type = row["EQUIPMENT TYPE"]
        if not pd.isna(expected_eq_type):
            assert node.equipment_type == expected_eq_type, f"Node {item_tag} equipment type mismatch"

