from __future__ import annotations

from pathlib import Path
from typing import Any

from app.agents.calculation_agent import CalculationAgent
from app.agents.intake_agent import IntakeAgent
from app.agents.sld_review_agent import SldReviewAgent
from app.agents.topology_agent import TopologyAgent


AGENTIC_CAPABILITIES = {
    "architecture": "multi_agent_orchestrated_pipeline",
    "course_concepts": [
        "specialized agents",
        "tool calling over deterministic engineering functions",
        "bounded Gemini vision/reasoning with fallback mode",
        "safety guardrails requiring source evidence",
    ],
    "safety_boundaries": [
        "consumer list remains the structured source of truth",
        "SLD PDF is used only as an independent visual cross-check",
        "Python tools own all numerical calculations",
        "Gemini must not invent tags, ratings, voltages, hierarchy, or issues",
    ],
}


class SingleLineReviewOrchestrator:
    """Coordinates specialized agents without changing the validated tools."""

    name = "singleline_review_orchestrator"

    def __init__(self) -> None:
        self.intake_agent = IntakeAgent()
        self.topology_agent = TopologyAgent()
        self.calculation_agent = CalculationAgent()
        self.sld_review_agent = SldReviewAgent()

    def run(
        self,
        consumer_list_path: Path,
        sld_pdf_path: Path,
        criteria_path: Path,
        is_demo: bool = False,
        input_filenames: dict | None = None,
    ) -> dict[str, Any]:
        trace: list[dict[str, Any]] = []

        intake = self.intake_agent.run(consumer_list_path, criteria_path)
        trace.append(self._trace(
            self.intake_agent.name,
            self.intake_agent.tools,
            {"items": len(intake.items), "criteria": sorted(intake.criteria.keys())},
        ))

        topology = self.topology_agent.run(intake.items)
        trace.append(self._trace(
            self.topology_agent.name,
            self.topology_agent.tools,
            {
                "nodes": len(topology["nodes"]),
                "edges": len(topology["edges"]),
                "missing_parents": len(topology["missing_parents"]),
                "cycles": len(topology["cycles"]),
            },
        ))

        nodes = self.calculation_agent.calculate(topology)
        deterministic_issues = self.calculation_agent.validate(intake.items, topology, nodes, intake.criteria)
        trace.append(self._trace(
            self.calculation_agent.name,
            self.calculation_agent.tools,
            {
                "calculated_nodes": len(nodes),
                "deterministic_issues": len(deterministic_issues),
            },
        ))

        sld_review = self.sld_review_agent.run(nodes, sld_pdf_path)
        trace.append(self._trace(
            self.sld_review_agent.name,
            self.sld_review_agent.tools,
            {
                "visual_assets": len(sld_review.assets),
                "sld_cross_check_issues": len(sld_review.issues),
            },
        ))

        kpis = self._build_kpis(intake.items, topology, nodes, deterministic_issues, sld_review.issues)
        if is_demo:
            kpis["synthetic_disclaimer"] = "All data is synthetic and anonymized."

        return {
            "items": intake.items,
            "topology": topology,
            "nodes": nodes,
            "edges": topology["edges"],
            "criteria": intake.criteria,
            "sld_assets": sld_review.assets,
            "deterministic_issues": deterministic_issues,
            "sld_cross_check_issues": sld_review.issues,
            "kpis": kpis,
            "is_demo": is_demo,
            "input_filenames": input_filenames or {},
            "agent_trace": trace,
            "agentic_capabilities": AGENTIC_CAPABILITIES,
        }

    @staticmethod
    def _trace(agent_name: str, tools: tuple[str, ...], evidence: dict[str, Any]) -> dict[str, Any]:
        return {
            "agent": agent_name,
            "tools_called": list(tools),
            "evidence": evidence,
        }

    @staticmethod
    def _build_kpis(items: list, topology: dict, nodes: list, deterministic_issues: list, sld_issues: list) -> dict:
        return {
            "electrical_assets": sum(1 for i in items if i.asset_role == "ELECTRICAL_ASSET"),
            "final_loads": sum(1 for i in items if i.asset_role == "FINAL_LOAD"),
            "total_connected_load_kw": round(sum((i.rated_power_kw or 0.0) for i in items if i.asset_role == "FINAL_LOAD"), 3),
            "nodes": len(nodes),
            "edges": len(topology["edges"]),
            "roots": topology["roots"],
            "missing_parents": topology["missing_parents"],
            "cycles": topology["cycles"],
            "deterministic_issues": len(deterministic_issues),
            "sld_cross_check_issues": len(sld_issues),
            "agentic_mode": "multi_agent_orchestrated",
        }
