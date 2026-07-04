from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from app.services.consumer_parser import parse_consumer_list
from app.services.criteria_parser import parse_design_criteria
from app.schemas import ConsumerItem


class IntakeResult(NamedTuple):
    items: list[ConsumerItem]
    criteria: dict


class IntakeAgent:
    """Validates and normalizes engineering input files.

    This is an agent boundary around deterministic parsing tools. It keeps the
    consumer list as the structured source of truth and exposes evidence about
    what was read for the orchestration trace.
    """

    name = "intake_agent"
    tools = ("parse_consumer_list", "parse_design_criteria")
    safety_rules = (
        "Only CSV/XLS/XLSX consumer lists are parsed as structured sources.",
        "No confidential project assumptions are inferred from filenames.",
    )

    def run(self, consumer_list_path: Path, criteria_path: Path) -> IntakeResult:
        items = parse_consumer_list(consumer_list_path)
        criteria = parse_design_criteria(criteria_path)
        return IntakeResult(items=items, criteria=criteria)
