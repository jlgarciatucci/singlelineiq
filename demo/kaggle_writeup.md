# SingleLineIQ: Agentic Electrical Single-Line Reviewer Powered by Gemini and Google Cloud

**Subtitle:** A Gemini-powered agent that reviews plant single-line diagrams against connected loads and explains design issues.

**Track:** Agents for Business

SingleLineIQ is an agentic electrical design reviewer for industrial projects. It reads a full-hierarchy consumer list, builds an electrical topology graph from `ITEM TAG` and `PARENT ITEM TAG`, calculates downstream loading, and uses the single-line diagram PDF as an independent visual cross-check.

Unlike a generic document chatbot, SingleLineIQ separates deterministic engineering calculations from LLM reasoning. Python validates the numbers; Gemini is used for visual SLD extraction and explanation.

The demo uses synthetic anonymized data only.

## Agent Architecture

The backend now runs through a multi-agent orchestration layer:

- `singleline_review_orchestrator` coordinates the workflow and records an agent trace.
- `intake_agent` validates and normalizes the consumer list and design criteria.
- `topology_agent` infers the network graph from parent-child tags without inventing assets.
- `calculation_agent` calls deterministic Python tools for downstream load aggregation and validation.
- `sld_review_agent` extracts or loads visual SLD assets and cross-checks them against the inferred graph.
- `reasoning_agent` and `report_review_agent` use bounded Gemini prompts when enabled, with template fallback when disabled.

This demonstrates three course concepts: specialized agents, tool-calling over domain functions, and safety boundaries around LLM reasoning. The guardrails are explicit: the consumer list is the source of truth, the SLD is a visual cross-check, Python owns all calculations, and Gemini must not invent tags, ratings, voltages, hierarchy, or issue IDs.
