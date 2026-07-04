from app import config
from app.services.consumer_parser import parse_consumer_list


def test_parse_consumer_list():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    assert len(items) == 144
    assert any(i.asset_role == "ELECTRICAL_ASSET" for i in items)
    assert any(i.asset_role == "FINAL_LOAD" for i in items)
    assert any(i.item_tag == "KPL2-MAIN-3300-TR00" for i in items)
