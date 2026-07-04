from unittest.mock import patch
from app import config
from app.services.sld_vision import extract_sld_assets


def test_extract_sld_assets_fallback():
    # Force Gemini disabled
    with patch("app.config.USE_GEMINI", False):
        assets = extract_sld_assets()
        assert len(assets) > 0
        assert any(a.item_tag == "KPL2-MAIN-3300-TR00" for a in assets)
        assert all(a.confidence > 0.0 for a in assets)


def test_extract_sld_assets_gemini_mode_mocked():
    mock_raw = [
        {
            "item_tag": "KPL2-MOCK-MCC",
            "asset_type": "MCC",
            "parent_tag": "KPL2-MOCK-SWBD",
            "voltage_kv": 0.4,
            "capacity_kw": 500.0,
            "confidence": 0.95,
            "notes": "Mocked note"
        }
    ]
    
    with patch("app.config.USE_GEMINI", True), \
         patch("app.config.GOOGLE_API_KEY", "mock_key"), \
         patch("app.services.gemini_client.extract_assets_from_pdf", return_value=mock_raw):
        
        assets = extract_sld_assets()
        assert len(assets) == 1
        asset = assets[0]
        assert asset.item_tag == "KPL2-MOCK-MCC"
        assert asset.asset_type == "MCC"
        assert asset.parent_tag == "KPL2-MOCK-SWBD"
        assert asset.voltage_kv == 0.4
        assert asset.capacity_kw == 500.0
        assert asset.confidence == 0.95
        assert asset.notes == "Mocked note"


def test_extract_sld_assets_gemini_mode_failure_fallback():
    # If Gemini client throws an exception, it should fallback to loading from CSV
    with patch("app.config.USE_GEMINI", True), \
         patch("app.config.GOOGLE_API_KEY", "mock_key"), \
         patch("app.services.gemini_client.extract_assets_from_pdf", side_effect=Exception("API failure")):
        
        assets = extract_sld_assets()
        assert len(assets) > 0
        # Ensure we loaded from the CSV fallback
        assert any(a.item_tag == "KPL2-MAIN-3300-TR00" for a in assets)
