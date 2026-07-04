from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

from app.schemas import SldAsset, TopologyNode, ValidationIssue
from app.services.cross_checker import cross_check_sld
from app.services.sld_vision import extract_sld_assets


class SldReviewResult(NamedTuple):
    assets: list[SldAsset]
    issues: list[ValidationIssue]


class SldReviewAgent:
    """Reviews the drawing extraction against the inferred structured topology."""

    name = "sld_review_agent"
    tools = ("extract_sld_assets", "cross_check_sld")
    safety_rules = (
        "Treat the SLD PDF as an independent visual cross-check only.",
        "Mark low-confidence visual extraction instead of fabricating certainty.",
    )

    def run(self, nodes: list[TopologyNode], sld_pdf_path: Path) -> SldReviewResult:
        assets = extract_sld_assets(sld_pdf_path=sld_pdf_path)
        issues = cross_check_sld(nodes, assets)
        return SldReviewResult(assets=assets, issues=issues)
