# SingleLineIQ

**Agentic Electrical Single-Line Reviewer** for the Kaggle AI Agents: Intensive Vibe Coding Capstone Project.

SingleLineIQ reviews a plant electrical design using the following core principles:

- **Synthetic & Anonymized Data**: All data in this repository (e.g., consumer lists, design criteria, diagrams) is strictly synthetic and anonymized. No confidential or real enterprise data is used.
- **Full Electrical Hierarchy**: The consumer list acts as the structured source of truth and contains all hierarchical levels—including transformers, switchboards, MCCs, distribution boards (DBs), and final loads—as individual rows.
- **Topology Inference**: The backend automatically infers the plant electrical topology graph directly from `ITEM TAG` and `PARENT ITEM TAG` relationships.
- **Visual Cross-Check**: The `SingleLineDiagram.pdf` is used strictly as an independent visual cross-check against the inferred topology graph.
- **No User SLD CSV Required**: The application does not require the user to provide an SLD topology CSV; all topology information is inferred or extracted.


## What is included

- FastAPI backend with deterministic engineering checks.
- Next.js frontend scaffold with dashboard/report pages.
- Synthetic full-hierarchy consumer list.
- Cleaned `SingleLineDiagram.pdf` for visual cross-checking.
- Fallback SLD visual extract CSV for reliable demo mode.
- Markdown report generation.
- Tests for parser, topology, calculations, validation, cross-check, and reporting.

## Core logic

```text
Consumer List CSV/XLSX
  -> parse rows
  -> build graph from ITEM TAG / PARENT ITEM TAG
  -> calculate downstream connected load
  -> run deterministic validation
  -> inspect SLD PDF with Gemini or fallback extract
  -> cross-check consumer graph vs visual graph
  -> generate dashboard and report
```

The app must **not** require an SLD topology CSV from the user.

## Quick start: backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/health
http://localhost:8000/api/demo/run
http://localhost:8000/api/report/markdown
```

## Quick start: frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

Set backend URL in `.env.local`:

```text
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Gemini mode

By default, the backend uses deterministic checks and a fallback CSV for SLD visual extraction.

To enable Gemini visual extraction later:

```text
USE_GEMINI=true
GOOGLE_API_KEY=your_key_here
USE_DEMO_SLD_EXTRACT=false
```

The Gemini implementation is intentionally guarded. Gemini may extract/describe visual SLD elements and explain known findings, but it must not invent equipment tags, ratings, or issues.

## Synthetic data disclaimer

All data in `data/synthetic` is synthetic and anonymized. It is not based on a real plant, client, project, or confidential engineering deliverable.

## Recommended Antigravity workflow

1. Open this folder in Antigravity.
2. Ask the agent to read `PRODUCT_BRIEF.md`, `AGENT_RULES.md`, and `ACCEPTANCE_TESTS.md` before coding.
3. Work milestone by milestone.
4. Do not allow broad refactors before tests pass.
5. Keep the rule: **infer topology from consumer list; use SLD PDF only as visual cross-check.**
