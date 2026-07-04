from __future__ import annotations
from pathlib import Path
import pandas as pd
from app.schemas import SldAsset


def load_demo_sld_extract(path: str | Path) -> list[SldAsset]:
    path = Path(path)
    if not path.exists():
        return []
    df = pd.read_csv(path)
    assets: list[SldAsset] = []
    # Flexible column normalization for generated benchmark CSVs.
    for _, row in df.iterrows():
        data = {str(k).strip().lower(): v for k, v in row.to_dict().items()}
        tag = data.get("item_tag") or data.get("asset_tag") or data.get("tag") or data.get("visible_asset") or data.get("visible_tag")
        if tag is None or pd.isna(tag):
            continue
        parent = data.get("parent_tag") or data.get("parent_item_tag") or data.get("visual_parent_tag") or data.get("visible_parent_tag")
        voltage = data.get("voltage_kv") or data.get("rated_voltage_kv") or data.get("voltage") or data.get("visible_voltage_kv")
        cap = data.get("capacity_kw") or data.get("rated_power") or data.get("rating_kw") or data.get("visible_rating_or_load_kw")
        conf = data.get("confidence") or 1.0
        def f(v):
            try:
                if pd.isna(v): return None
                return float(v)
            except Exception:
                return None
        assets.append(SldAsset(
            item_tag=str(tag),
            asset_type=str(data.get("asset_type") or data.get("equipment_type") or data.get("visible_type") or "unknown"),
            parent_tag=None if parent is None or pd.isna(parent) else str(parent),
            voltage_kv=f(voltage),
            capacity_kw=f(cap),
            confidence=float(conf) if str(conf) != "nan" else 1.0,
            notes=None if data.get("notes") is None else str(data.get("notes")),
        ))
    return assets

def analyze_sld_pdf_with_gemini(pdf_path: str | Path) -> list[SldAsset]:
    from app.services.gemini_client import extract_assets_from_pdf
    raw_assets = extract_assets_from_pdf(str(pdf_path))
    assets = []
    for a in raw_assets:
        tag = a.get("item_tag")
        if not tag:
            continue
        assets.append(SldAsset(
            item_tag=str(tag),
            asset_type=str(a.get("asset_type") or "unknown"),
            parent_tag=None if not a.get("parent_tag") else str(a.get("parent_tag")),
            voltage_kv=a.get("voltage_kv"),
            capacity_kw=a.get("capacity_kw"),
            confidence=float(a.get("confidence") or 1.0),
            notes=a.get("notes"),
        ))
    return assets

def extract_sld_assets() -> list[SldAsset]:
    from app import config
    if config.USE_GEMINI and config.GOOGLE_API_KEY:
        try:
            return analyze_sld_pdf_with_gemini(config.SLD_PDF_FILE)
        except Exception as e:
            print(f"Gemini visual extraction failed: {e}. Falling back to demo CSV.")
            return load_demo_sld_extract(config.SLD_EXTRACT_FILE)
    else:
        return load_demo_sld_extract(config.SLD_EXTRACT_FILE)
