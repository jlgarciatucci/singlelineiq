from __future__ import annotations
from pathlib import Path
import math
import pandas as pd
from app.schemas import ConsumerItem

COLUMN_MAP = {
    "REVISION": "revision",
    "DATA STATUS": "data_status",
    "LOCATION": "location",
    "PARENT EQUIPMENT": "parent_equipment",
    "PARENT ITEM TAG": "parent_item_tag",
    "ASSET ROLE": "asset_role",
    "ITEM TAG": "item_tag",
    "DESCRIPTION": "description",
    "PANEL LOCATION": "panel_location",
    "PANEL TAG": "panel_tag",
    "SUPPLY BUS": "supply_bus",
    "EQUIPMENT TYPE": "equipment_type",
    "STARTER TYPE": "starter_type",
    "TYPICAL SCHEMATIC": "typical_schematic",
    "CLASS": "class",
    "DUTY": "duty",
    "COINCIDENCE FACTOR": "coincidence_factor",
    "SUPPLY AC/DC": "supply_ac_dc",
    "PHASE ARRANGEMENT": "phase_arrangement",
    "RATED VOLTAGE [kV]": "rated_voltage_kv",
    "POWER FACTOR AT DEMAND": "power_factor_at_demand",
    "EFFICIENCY AT DEMAND": "efficiency_at_demand",
    "RATED POWER": "rated_power_kw",
    "RATED UOM": "rated_uom",
    "ABSORBED POWER": "absorbed_power_kw",
    "ABSORBED UOM": "absorbed_uom",
    "DEMAND FACTOR": "demand_factor",
    "ELEC. CONSUMED POWER": "elec_consumed_power_kw",
    "CONSUMED UOM": "consumed_uom",
    "FULL LOAD CURRENT [A]": "full_load_current_a",
    "HAZARDOUS AREA": "hazardous_area",
    "EXPLOSION PROTECTION": "explosion_protection",
    "SUBTATION": "substation",
    "CABL LENGTH": "cable_length",
    "PARENT TRANSFORMER OF PANEL OR DIREC FEEDER (FDR)": "parent_transformer_or_feeder",
    "REMARKS": "remarks",
    "SPID": "spid",
}
NUMERIC_COLUMNS = {
    "coincidence_factor", "rated_voltage_kv", "power_factor_at_demand",
    "efficiency_at_demand", "rated_power_kw", "absorbed_power_kw",
    "demand_factor", "elec_consumed_power_kw", "full_load_current_a", "cable_length"
}

def _clean_value(value):
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except TypeError:
        pass
    if isinstance(value, str):
        value = value.strip()
        if value == "" or value.lower() in {"nan", "none", "null"}:
            return None
        return value
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

def _to_float(value):
    value = _clean_value(value)
    if value is None:
        return None
    if isinstance(value, str):
        value = value.replace(",", ".")
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def load_dataframe(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)

def parse_consumer_list(path: str | Path) -> list[ConsumerItem]:
    df = load_dataframe(path)
    missing = [c for c in ["ITEM TAG", "ASSET ROLE"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    items: list[ConsumerItem] = []
    for _, row in df.iterrows():
        raw = {str(k): _clean_value(v) for k, v in row.to_dict().items()}
        data = {}
        for original, field in COLUMN_MAP.items():
            if original in raw:
                data[field] = raw[original]
        for col in NUMERIC_COLUMNS:
            if col in data:
                data[col] = _to_float(data[col])
        data["raw"] = raw
        item = ConsumerItem.model_validate(data)
        items.append(item)
    return items
