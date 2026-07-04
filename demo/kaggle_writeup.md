# SingleLineIQ: Agentic Electrical Single-Line Reviewer Powered by Gemini and Google Cloud

**Subtitle:** A Gemini-powered agent that reviews plant single-line diagrams against connected loads and explains design issues.

**Track:** Agents for Business

SingleLineIQ is an agentic electrical design reviewer for industrial projects. It reads a full-hierarchy consumer list, builds an electrical topology graph from `ITEM TAG` and `PARENT ITEM TAG`, calculates downstream loading, and uses the single-line diagram PDF as an independent visual cross-check.

Unlike a generic document chatbot, SingleLineIQ separates deterministic engineering calculations from LLM reasoning. Python validates the numbers; Gemini is used for visual SLD extraction and explanation.

The demo uses synthetic anonymized data only.
