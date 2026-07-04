from __future__ import annotations
from typing import Any, Literal
from pydantic import BaseModel, Field

AssetRole = Literal["ELECTRICAL_ASSET", "FINAL_LOAD"]
Severity = Literal["low", "medium", "high", "critical"]

class ConsumerItem(BaseModel):
    revision: str | None = None
    data_status: str | None = None
    location: str | None = None
    parent_equipment: str | None = None
    parent_item_tag: str | None = None
    asset_role: str
    item_tag: str
    description: str | None = None
    panel_location: str | None = None
    panel_tag: str | None = None
    supply_bus: str | None = None
    equipment_type: str | None = None
    starter_type: str | None = None
    typical_schematic: str | None = None
    class_: str | None = Field(default=None, alias="class")
    duty: str | None = None
    coincidence_factor: float | None = None
    supply_ac_dc: str | None = None
    phase_arrangement: str | None = None
    rated_voltage_kv: float | None = None
    power_factor_at_demand: float | None = None
    efficiency_at_demand: float | None = None
    rated_power_kw: float | None = None
    rated_uom: str | None = None
    absorbed_power_kw: float | None = None
    absorbed_uom: str | None = None
    demand_factor: float | None = None
    elec_consumed_power_kw: float | None = None
    consumed_uom: str | None = None
    full_load_current_a: float | None = None
    hazardous_area: str | None = None
    explosion_protection: str | None = None
    substation: str | None = None
    cable_length: float | None = None
    parent_transformer_or_feeder: str | None = None
    remarks: str | None = None
    spid: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)

class TopologyNode(BaseModel):
    node_id: str
    parent_id: str | None = None
    asset_role: str
    equipment_type: str | None = None
    description: str | None = None
    voltage_kv: float | None = None
    capacity_kw: float | None = None
    direct_load_kw: float = 0.0
    downstream_load_kw: float = 0.0
    downstream_final_load_count: int = 0
    downstream_vsd_count: int = 0
    vsd_percent: float = 0.0
    utilization_percent: float | None = None
    largest_downstream_load_kw: float | None = None
    largest_downstream_load_tag: str | None = None
    status: Literal["normal", "warning", "critical", "unknown"] = "unknown"
    path: list[str] = Field(default_factory=list)

class TopologyEdge(BaseModel):
    parent_id: str
    child_id: str

class ValidationIssue(BaseModel):
    issue_id: str
    severity: Severity
    issue_type: str
    title: str
    item_tag: str | None = None
    parent_tag: str | None = None
    evidence: dict[str, Any] = Field(default_factory=dict)
    recommendation: str
    source: str
    confidence: float | None = None

class SldAsset(BaseModel):
    item_tag: str
    asset_type: str | None = None
    parent_tag: str | None = None
    voltage_kv: float | None = None
    capacity_kw: float | None = None
    confidence: float = 1.0
    notes: str | None = None

class DemoResult(BaseModel):
    kpis: dict[str, Any]
    nodes: list[TopologyNode]
    edges: list[TopologyEdge]
    deterministic_issues: list[ValidationIssue]
    sld_cross_check_issues: list[ValidationIssue]
