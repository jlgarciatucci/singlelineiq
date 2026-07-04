from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
import csv
import io

from app import config
from app.services.consumer_parser import parse_consumer_list
from app.services.criteria_parser import parse_design_criteria
from app.services.topology_inference import build_topology
from app.services.load_calculator import calculate_loads
from app.services.deterministic_validator import validate
from app.services.sld_vision import extract_sld_assets
from app.services.cross_checker import cross_check_sld
from app.services.report_generator import generate_markdown_report

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SingleLineIQ API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_pipeline() -> dict:
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    criteria = parse_design_criteria(config.DESIGN_CRITERIA_FILE)
    topology = build_topology(items)
    nodes = calculate_loads(topology)
    deterministic_issues = validate(items, topology, nodes, criteria)
    sld_assets = extract_sld_assets()
    sld_cross_check_issues = cross_check_sld(nodes, sld_assets)
    kpis = {
        "electrical_assets": sum(1 for i in items if i.asset_role == "ELECTRICAL_ASSET"),
        "final_loads": sum(1 for i in items if i.asset_role == "FINAL_LOAD"),
        "total_connected_load_kw": round(sum((i.rated_power_kw or 0.0) for i in items if i.asset_role == "FINAL_LOAD"), 3),
        "nodes": len(nodes),
        "edges": len(topology["edges"]),
        "roots": topology["roots"],
        "missing_parents": topology["missing_parents"],
        "cycles": topology["cycles"],
        "deterministic_issues": len(deterministic_issues),
        "sld_cross_check_issues": len(sld_cross_check_issues),
        "synthetic_disclaimer": "All data is synthetic and anonymized.",
    }
    return {
        "items": items,
        "topology": topology,
        "nodes": nodes,
        "edges": topology["edges"],
        "criteria": criteria,
        "sld_assets": sld_assets,
        "deterministic_issues": deterministic_issues,
        "sld_cross_check_issues": sld_cross_check_issues,
        "kpis": kpis,
    }

@app.get("/health")
def health():
    return {"status": "ok", "app": config.APP_NAME}

@app.get("/api/demo/run")
def demo_run():
    r = run_pipeline()
    return {
        "kpis": r["kpis"],
        "nodes": [n.model_dump() for n in r["nodes"]],
        "edges": [e.model_dump() for e in r["edges"]],
        "deterministic_issues": [i.model_dump() for i in r["deterministic_issues"]],
        "sld_cross_check_issues": [i.model_dump() for i in r["sld_cross_check_issues"]],
        "sld_assets": [a.model_dump() for a in r["sld_assets"]],
    }

@app.get("/api/consumer-list")
def consumer_list():
    items = parse_consumer_list(config.CONSUMER_LIST_FILE)
    return [i.model_dump() for i in items]

@app.get("/api/topology")
def topology():
    r = run_pipeline()
    return {"nodes": [n.model_dump() for n in r["nodes"]], "edges": [e.model_dump() for e in r["edges"]], "kpis": r["kpis"]}

@app.get("/api/load-summary")
def load_summary():
    r = run_pipeline()
    nodes = [n for n in r["nodes"] if n.asset_role == "ELECTRICAL_ASSET"]
    return [n.model_dump() for n in sorted(nodes, key=lambda n: n.downstream_load_kw, reverse=True)]

@app.get("/api/issues/deterministic")
def deterministic_issues():
    r = run_pipeline()
    return [i.model_dump() for i in r["deterministic_issues"]]

@app.get("/api/sld/cross-check")
def sld_cross_check():
    r = run_pipeline()
    return [i.model_dump() for i in r["sld_cross_check_issues"]]

@app.get("/api/sld/pdf")
def sld_pdf():
    if not config.SLD_PDF_FILE.exists():
        raise HTTPException(status_code=404, detail="SLD PDF not found")
    return FileResponse(config.SLD_PDF_FILE, media_type="application/pdf", filename="SingleLineDiagram.pdf")

from app.agents.reasoning_agent import explain_issues
from app.agents.report_review_agent import review_report
from app.services.pdf_generator import generate_enriched_pdf_report


@app.get("/api/report/pdf")
def report_pdf():
    r = run_pipeline()
    all_issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    explanations = explain_issues(all_issues, r["kpis"], r["nodes"])
    pdf_bytes = generate_enriched_pdf_report(
        r["kpis"],
        r["nodes"],
        r["deterministic_issues"],
        r["sld_cross_check_issues"],
        explanations
    )
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=singlelineiq_report.pdf"}
    )


@app.get("/api/report/markdown", response_class=PlainTextResponse)
def report_markdown():
    r = run_pipeline()
    all_issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    explanations = explain_issues(all_issues, r["kpis"], r["nodes"])
    report = generate_markdown_report(r["kpis"], r["nodes"], r["deterministic_issues"], r["sld_cross_check_issues"], explanations)
    reviewed = review_report(report)
    return reviewed

@app.get("/api/report/issues.csv")
def report_issues_csv():
    r = run_pipeline()
    issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["issue_id", "severity", "issue_type", "title", "item_tag", "parent_tag", "source", "confidence", "recommendation"])
    writer.writeheader()
    for i in issues:
        writer.writerow({k: getattr(i, k) for k in writer.fieldnames})
    buf.seek(0)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=singlelineiq_issues.csv"})
