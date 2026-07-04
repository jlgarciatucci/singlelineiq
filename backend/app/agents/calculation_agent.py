from __future__ import annotations

from app.schemas import TopologyNode
from app.services.load_calculator import calculate_loads
from app.services.deterministic_validator import validate


class CalculationAgent:
    """Runs deterministic load aggregation and rule validation tools."""

    name = "calculation_agent"
    tools = ("calculate_loads", "validate")
    safety_rules = (
        "Python calculations are the source of truth for numerical checks.",
        "Every issue must include deterministic evidence.",
    )

    def calculate(self, topology: dict) -> list[TopologyNode]:
        return calculate_loads(topology)

    def validate(self, items: list, topology: dict, nodes: list[TopologyNode], criteria: dict) -> list:
        return validate(items, topology, nodes, criteria)
