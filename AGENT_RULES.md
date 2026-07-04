# Agent Rules

1. Use only synthetic anonymized data.
2. Do not use confidential or real enterprise data.
3. The consumer list is the source of truth for structured topology.
4. The SLD PDF is only a visual cross-check.
5. Do not ask the user for SLD topology CSV.
6. Infer topology from `ITEM TAG` and `PARENT ITEM TAG`.
7. Python calculations are the source of truth for numerical checks.
8. Gemini may extract visual SLD information and explain findings.
9. Gemini must not invent equipment tags, ratings, voltages, or hierarchy.
10. Every issue must include evidence.
11. If visual extraction is uncertain, mark the issue as uncertain.
12. The report must separate facts, calculations, visual observations, and recommendations.
13. Keep the MVP reliable and demo-ready.
