# Development Plan

## Milestone 1: Scaffold
- FastAPI backend
- Next.js frontend
- Synthetic data folder
- Basic health endpoint

## Milestone 2: Consumer parser
- Load consumer CSV/XLSX
- Normalize fields
- Distinguish electrical assets and final loads

## Milestone 3: Topology inference
- Build graph from `ITEM TAG` and `PARENT ITEM TAG`
- Detect root/orphan/missing parent/cycles

## Milestone 4: Electrical calculations
- Downstream load by asset
- Capacity usage
- VSD concentration
- Largest downstream load

## Milestone 5: Deterministic validation
- Duplicate tags
- Missing rated power
- Missing/invalid parents
- Overload checks
- High VSD concentration
- Invalid hierarchy

## Milestone 6: SLD visual extraction
- Gemini mode when configured
- Fallback visual extract mode for reliable demo

## Milestone 7: Cross-check
- Consumer graph vs visual SLD graph
- Missing-in-SLD
- SLD-only assets
- Parent mismatches
- Rating/voltage mismatches

## Milestone 8: Frontend dashboard
- KPI summary
- Topology tree
- Issue cards
- SLD preview
- Report viewer

## Milestone 9: Deploy and demo
- Cloud Run backend
- Vercel or Cloud Run frontend
- Kaggle writeup/video
