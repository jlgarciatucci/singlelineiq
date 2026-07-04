from __future__ import annotations
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse, PlainTextResponse, StreamingResponse
import csv
import io
import uuid
import shutil
import tempfile
from pathlib import Path

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

app = FastAPI(title="SingleLineIQ API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Session storage: maps session_id -> { dir, consumer_list_path, sld_pdf_path, filenames }
# ---------------------------------------------------------------------------
_sessions: dict[str, dict] = {}


def _get_session(session_id: str) -> dict:
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found. Please upload files first.")
    return _sessions[session_id]


# ---------------------------------------------------------------------------
# Pipeline runner (parameterized)
# ---------------------------------------------------------------------------
def run_pipeline(
    consumer_list_path: Path | None = None,
    sld_pdf_path: Path | None = None,
    criteria_path: Path | None = None,
    is_demo: bool = False,
    input_filenames: dict | None = None,
) -> dict:
    cl_path = consumer_list_path or config.CONSUMER_LIST_FILE
    cr_path = criteria_path or config.DESIGN_CRITERIA_FILE
    sld_path = sld_pdf_path or config.SLD_PDF_FILE

    items = parse_consumer_list(cl_path)
    criteria = parse_design_criteria(cr_path)
    topology = build_topology(items)
    nodes = calculate_loads(topology)
    deterministic_issues = validate(items, topology, nodes, criteria)
    sld_assets = extract_sld_assets(sld_pdf_path=sld_path)
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
        "is_demo": is_demo,
        "input_filenames": input_filenames or {},
    }


# ---------------------------------------------------------------------------
# Upload endpoint
# ---------------------------------------------------------------------------
ALLOWED_CONSUMER_EXTS = {".csv", ".xlsx", ".xlsm", ".xls"}
ALLOWED_SLD_EXTS = {".pdf"}


@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    if len(files) != 2:
        raise HTTPException(
            status_code=400,
            detail=f"Exactly 2 files required (Consumer List CSV/XLSX + SLD PDF). Got {len(files)}.",
        )

    consumer_file = None
    sld_file = None

    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext in ALLOWED_CONSUMER_EXTS:
            if consumer_file is not None:
                raise HTTPException(status_code=400, detail="Two consumer list files detected. Please provide exactly one CSV/XLSX and one PDF.")
            consumer_file = f
        elif ext in ALLOWED_SLD_EXTS:
            if sld_file is not None:
                raise HTTPException(status_code=400, detail="Two PDF files detected. Please provide exactly one CSV/XLSX and one PDF.")
            sld_file = f
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: '{ext}'. Accepted: CSV/XLSX for consumer list, PDF for SLD.")

    if consumer_file is None:
        raise HTTPException(status_code=400, detail="Missing consumer list file (CSV or XLSX).")
    if sld_file is None:
        raise HTTPException(status_code=400, detail="Missing SLD PDF file.")

    # Create session directory
    session_id = str(uuid.uuid4())[:8]
    session_dir = Path(tempfile.mkdtemp(prefix=f"sliq_{session_id}_"))

    # Save consumer list
    cl_path = session_dir / consumer_file.filename
    with open(cl_path, "wb") as out:
        shutil.copyfileobj(consumer_file.file, out)

    # Save SLD PDF
    sld_path = session_dir / sld_file.filename
    with open(sld_path, "wb") as out:
        shutil.copyfileobj(sld_file.file, out)

    _sessions[session_id] = {
        "dir": session_dir,
        "consumer_list_path": cl_path,
        "sld_pdf_path": sld_path,
        "filenames": {
            "consumer_list": consumer_file.filename,
            "sld_pdf": sld_file.filename,
        },
    }

    return {
        "session_id": session_id,
        "files": {
            "consumer_list": consumer_file.filename,
            "sld_pdf": sld_file.filename,
        },
        "message": "Files uploaded successfully. Call POST /api/analyze to run the pipeline.",
    }


# ---------------------------------------------------------------------------
# Analyze endpoint (primary — uses uploaded files)
# ---------------------------------------------------------------------------
@app.post("/api/analyze")
def analyze(session_id: str = Query(...)):
    sess = _get_session(session_id)
    r = run_pipeline(
        consumer_list_path=sess["consumer_list_path"],
        sld_pdf_path=sess["sld_pdf_path"],
        is_demo=False,
        input_filenames=sess["filenames"],
    )
    return {
        "kpis": r["kpis"],
        "nodes": [n.model_dump() for n in r["nodes"]],
        "edges": [e.model_dump() for e in r["edges"]],
        "deterministic_issues": [i.model_dump() for i in r["deterministic_issues"]],
        "sld_cross_check_issues": [i.model_dump() for i in r["sld_cross_check_issues"]],
        "sld_assets": [a.model_dump() for a in r["sld_assets"]],
        "session_id": session_id,
    }


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok", "app": config.APP_NAME}


# ---------------------------------------------------------------------------
# Demo endpoint (fallback for testing — uses hardcoded data)
# ---------------------------------------------------------------------------
@app.get("/api/demo/run")
def demo_run():
    r = run_pipeline(
        is_demo=True,
        input_filenames={
            "consumer_list": config.CONSUMER_LIST_FILE.name,
            "sld_pdf": config.SLD_PDF_FILE.name,
        },
    )
    return {
        "kpis": r["kpis"],
        "nodes": [n.model_dump() for n in r["nodes"]],
        "edges": [e.model_dump() for e in r["edges"]],
        "deterministic_issues": [i.model_dump() for i in r["deterministic_issues"]],
        "sld_cross_check_issues": [i.model_dump() for i in r["sld_cross_check_issues"]],
        "sld_assets": [a.model_dump() for a in r["sld_assets"]],
    }


# ---------------------------------------------------------------------------
# SLD PDF viewer (session-aware)
# ---------------------------------------------------------------------------
@app.get("/api/sld/pdf")
def sld_pdf(session_id: str | None = Query(None)):
    if session_id:
        sess = _get_session(session_id)
        pdf_path = sess["sld_pdf_path"]
    else:
        pdf_path = config.SLD_PDF_FILE
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="SLD PDF not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename="SingleLineDiagram.pdf")


# ---------------------------------------------------------------------------
# Reports (session-aware)
# ---------------------------------------------------------------------------
from app.agents.reasoning_agent import explain_issues
from app.agents.report_review_agent import review_report
from app.services.pdf_generator import generate_enriched_pdf_report


def _run_pipeline_for_session(session_id: str | None) -> dict:
    """Helper: run pipeline for a session or fall back to demo data."""
    if session_id:
        sess = _get_session(session_id)
        return run_pipeline(
            consumer_list_path=sess["consumer_list_path"],
            sld_pdf_path=sess["sld_pdf_path"],
            is_demo=False,
            input_filenames=sess["filenames"],
        )
    else:
        return run_pipeline(
            is_demo=True,
            input_filenames={
                "consumer_list": config.CONSUMER_LIST_FILE.name,
                "sld_pdf": config.SLD_PDF_FILE.name,
            },
        )


@app.get("/api/report/pdf")
def report_pdf(session_id: str | None = Query(None)):
    r = _run_pipeline_for_session(session_id)
    all_issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    explanations = explain_issues(all_issues, r["kpis"], r["nodes"])
    pdf_bytes = generate_enriched_pdf_report(
        r["kpis"],
        r["nodes"],
        r["deterministic_issues"],
        r["sld_cross_check_issues"],
        explanations,
        input_filenames=r["input_filenames"],
        is_demo=r["is_demo"],
    )
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=singlelineiq_report.pdf"}
    )


@app.get("/api/report/markdown", response_class=PlainTextResponse)
def report_markdown(session_id: str | None = Query(None)):
    r = _run_pipeline_for_session(session_id)
    all_issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    explanations = explain_issues(all_issues, r["kpis"], r["nodes"])
    report = generate_markdown_report(
        r["kpis"],
        r["nodes"],
        r["deterministic_issues"],
        r["sld_cross_check_issues"],
        explanations,
        input_filenames=r["input_filenames"],
        is_demo=r["is_demo"],
    )
    reviewed = review_report(report)
    return reviewed


@app.get("/api/report/issues.csv")
def report_issues_csv(session_id: str | None = Query(None)):
    r = _run_pipeline_for_session(session_id)
    issues = r["deterministic_issues"] + r["sld_cross_check_issues"]
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["issue_id", "severity", "issue_type", "title", "item_tag", "parent_tag", "source", "confidence", "recommendation"])
    writer.writeheader()
    for i in issues:
        writer.writerow({k: getattr(i, k) for k in writer.fieldnames})
    buf.seek(0)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=singlelineiq_issues.csv"})
