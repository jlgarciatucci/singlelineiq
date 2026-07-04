from __future__ import annotations

from app.schemas import ConsumerItem
from app.services.topology_inference import build_topology


class TopologyAgent:
    """Infers the electrical hierarchy from parent-child item tags."""

    name = "topology_agent"
    tools = ("build_topology",)
    safety_rules = (
        "Use ITEM TAG and PARENT ITEM TAG only for structured hierarchy.",
        "Report missing parents and cycles instead of inventing upstream assets.",
    )

    def run(self, items: list[ConsumerItem]) -> dict:
        return build_topology(items)
