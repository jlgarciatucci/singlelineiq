from __future__ import annotations
from pathlib import Path
import pandas as pd

DEFAULT_CRITERIA = {
    "asset_overload_warning_percent": 85.0,
    "asset_overload_critical_percent": 100.0,
    "high_vsd_concentration_percent": 70.0,
}

def parse_design_criteria(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return DEFAULT_CRITERIA.copy()
    df = pd.read_csv(path)
    criteria = DEFAULT_CRITERIA.copy()
    # Supports both generic key/value CSV and custom benchmark table.
    lower_cols = {c.lower(): c for c in df.columns}
    key_col = lower_cols.get("key") or lower_cols.get("criterion") or lower_cols.get("name")
    value_col = lower_cols.get("value") or lower_cols.get("threshold")
    if key_col and value_col:
        for _, row in df.iterrows():
            key = str(row[key_col]).strip()
            value = row[value_col]
            try:
                value = float(value)
            except Exception:
                pass
            if key:
                criteria[key] = value
    return criteria
