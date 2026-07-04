# Acceptance Tests

The MVP passes if:

1. It loads the v15 full-hierarchy consumer list.
2. It loads the v15 design criteria.
3. It reads every electrical asset and final load row.
4. It builds a graph from `ITEM TAG` and `PARENT ITEM TAG`.
5. It calculates downstream load for MCCs, DBs, switchboards, transformers, and main boards.
6. It detects overloaded assets.
7. It detects duplicate item tags.
8. It detects missing rated power.
9. It detects invalid parent relationships.
10. It analyzes `SingleLineDiagram.pdf` visually or uses fallback visual extraction.
11. It detects consumer-list assets missing from the SLD.
12. It detects SLD-only assets.
13. It detects wrong-parent visual mismatches.
14. It generates issue cards with severity, evidence, and recommendation.
15. It generates a Markdown engineering report.
16. The frontend shows dashboard, topology, SLD preview, issues, and report.
17. The app clearly states the data is synthetic and anonymized.
