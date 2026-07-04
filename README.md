![](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F4591020%2Fd61e20dc219fc3e0e40fbc7364b52bf6%2FSingleLineIQ.png?generation=1783183071600519&alt=media)

# SingleLineIQ: Agentic Electrical Single-Line Reviewer Powered by Gemini and Google Cloud

**Subtitle:** A multi-agent engineering reviewer that reads electrical deliverables, reconstructs topology, validates connected loads, cross-checks the SLD, and generates an evidence-backed action report.

**Track:** Agents for Business

## Project Summary

SingleLineIQ is an agentic electrical design-review app for industrial power distribution projects. It reviews two common engineering deliverables:

- A full-hierarchy electrical consumer/load list in CSV or Excel format.
- A CAD-exported electrical single-line diagram PDF.

The app reconstructs the plant electrical hierarchy, calculates downstream connected loads, detects inconsistencies, asks Gemini 2.5 Flash to visually inspect the SLD PDF, and generates a professional engineering review report.

The goal is not to build a generic document chatbot. The goal is to automate a real review workflow that electrical engineers perform manually: compare the drawing against the load list, check the network hierarchy, calculate connected loading, identify mismatches, and produce a traceable list of issues.

All demo data is synthetic and anonymized.

## The Problem

Industrial electrical projects usually rely on several documents that evolve independently:

- Single-line diagrams.
- Consumer lists and load schedules.
- MCC and switchboard schedules.
- Transformer ratings.
- Design criteria and tagging standards.

Even when each document looks correct in isolation, mismatches can appear between them. Typical examples include:

- A board or MCC exists in the consumer list but is not visible in the SLD.
- Equipment appears in the SLD but is missing from the structured load list.
- A feeder has a different parent in the drawing than in the spreadsheet.
- A child load has a voltage that does not match the upstream asset.
- An MCC has too much downstream connected load.
- A board has a high concentration of VSD-driven loads.
- Tags are duplicated or parent references are missing.

These issues are often caught by manual spreadsheet checks and drawing markups. That work is valuable, but repetitive and error-prone. SingleLineIQ turns it into an agentic verification workflow.

## What The App Does

The deployed web app lets the user upload:

1. A consumer list file.
2. A single-line diagram PDF.

The backend then runs a multi-agent review:

1. Normalize the consumer list.
2. Infer the electrical topology from `ITEM TAG` and `PARENT ITEM TAG`.
3. Calculate downstream connected load recursively.
4. Run deterministic validation rules.
5. Use Gemini 2.5 Flash to extract visible SLD assets from the PDF.
6. Cross-check the visual SLD extraction against the structured topology.
7. Generate dashboard KPIs, issue cards, topology views, CSV exports, Markdown reports, and PDF reports.

The result is an interactive dashboard with:

- Electrical asset and load counts.
- Total connected load.
- Top loaded assets.
- Inferred topology tree.
- Deterministic engineering findings.
- Visual SLD cross-check findings.
- SLD PDF preview.
- Downloadable engineering report.

## Agentic Architecture

SingleLineIQ uses a multi-agent orchestration layer around deterministic engineering tools. The agents are specialized, but the numerical work remains grounded in Python calculations.

```text
                     SingleLineIQ Agentic Review Chain

  User Uploads
  CSV/XLSX + PDF
       |
       v
  +-------------------------------+
  | SingleLine Review Orchestrator|
  | records trace + coordinates   |
  +-------------------------------+
       |
       +--> Intake Agent
       |    tools: parse_consumer_list, parse_design_criteria
       |
       +--> Topology Agent
       |    tool: build_topology from ITEM TAG / PARENT ITEM TAG
       |
       +--> Calculation Agent
       |    tools: calculate_loads, validate
       |
       +--> SLD Review Agent
       |    tools: Gemini 2.5 Flash PDF extraction, cross_check_sld
       |
       +--> Report Layer
            tools: evidence-backed Markdown/PDF generation
```

| Layer | Agent | What It Produces |
|---|---|---|
| 1 | Intake Agent | Normalized consumer list and criteria |
| 2 | Topology Agent | Electrical graph nodes, edges, roots, missing parents, cycles |
| 3 | Calculation Agent | Downstream load, utilization, VSD concentration, deterministic issues |
| 4 | SLD Review Agent | Visual asset extraction and SLD cross-check findings |
| 5 | Report Layer | Dashboard data, CSV export, Markdown report, PDF report |

### Agents

**SingleLine Review Orchestrator**  
Coordinates the full workflow and records an agent trace.

**Intake Agent**  
Validates and normalizes uploaded files. The consumer list is treated as the structured source of truth.

**Topology Agent**  
Builds the electrical hierarchy from `ITEM TAG` and `PARENT ITEM TAG`. It reports missing parents and cycles rather than inventing assets.

**Calculation Agent**  
Runs deterministic Python tools for load aggregation and validation. This keeps engineering calculations outside the LLM.

**SLD Review Agent**  
Uses Gemini 2.5 Flash to inspect the uploaded SLD PDF and extract visible equipment tags, parent relationships, ratings, voltage levels, and confidence notes.

**Reasoning / Report Layer**  
Turns evidence-backed issues into a readable engineering report while preserving issue IDs, tags, ratings, and source evidence.

## System Design

```text
                             Google Cloud Run Deployment

  +---------------------+                         +----------------------+
  | Next.js Frontend    |                         | FastAPI Backend      |
  | Cloud Run           |  upload/analyze/report  | Cloud Run            |
  |                     | ----------------------> |                      |
  | Dashboard           |                         | Multi-agent pipeline |
  | SLD viewer          | <---------------------- | Report endpoints     |
  | Report viewer       |       JSON/PDF/CSV      | Session cache        |
  +---------------------+                         +----------+-----------+
                                                            |
                                                            v
       +------------------------+       +-------------------+-------------------+
       | Python Engineering     |       | Gemini 2.5 Flash                     |
       | Tools                  |       | Visual SLD extraction                |
       |                        |       |                                      |
       | parse CSV/XLSX         |       | read PDF diagram                     |
       | infer topology         |       | extract tags, parents, ratings       |
       | calculate loads        |       | return confidence + notes            |
       | validate issues        |       +-------------------+------------------+
       +-----------+------------+                           |
                   |                                        |
                   +----------------+-----------------------+
                                    v
                         Evidence-backed issue database
                                    |
                                    v
                         Dashboard + Engineering Report
```

The deployed stack is:

- **Frontend:** Next.js dashboard on Cloud Run.
- **Backend:** FastAPI service on Cloud Run.
- **Model:** Gemini 2.5 Flash through the Gemini API.
- **Core tools:** Python parsers, graph inference, load aggregation, validation, SLD cross-checking, and report generation.
- **Data:** Synthetic anonymized electrical design dataset.

## Why This Is Agentic

SingleLineIQ is not only a form upload app and not only an LLM prompt. It demonstrates several agent-course concepts:

1. **Specialized agents:** separate intake, topology, calculation, SLD review, and reporting responsibilities.
2. **Tool use:** agents call deterministic domain tools rather than relying only on model text generation.
3. **Multimodal reasoning:** Gemini 2.5 Flash analyzes the SLD PDF visually.
4. **Stateful workflow:** uploaded files create a session, analysis results are cached, and reports reuse the completed agentic analysis.
5. **Safety guardrails:** LLM output is constrained by evidence, and calculations remain deterministic.
6. **Cloud deployment:** both frontend and backend are publicly deployed on Google Cloud Run.

## Safety And Grounding

Electrical engineering recommendations must be grounded. SingleLineIQ uses strict boundaries:

- The consumer list is the structured source of truth.
- The SLD PDF is an independent visual cross-check, not the authoritative database.
- Python calculations own all numerical checks.
- Gemini must not invent equipment tags, ratings, voltages, hierarchy, or issue IDs.
- Every issue includes evidence.
- Low-confidence visual extraction is surfaced as uncertainty.
- The report separates facts, calculations, visual observations, and recommendations.
- The app explicitly states that it does not perform load flow, short-circuit, motor starting, protection coordination, or arc-flash studies.

This makes the app useful as an engineering assistant while still respecting professional review boundaries.

## Example Findings

SingleLineIQ can identify findings such as:

| Finding Type | Example Evidence | Engineering Meaning |
|---|---|---|
| Asset overload | Downstream load exceeds asset capacity | Equipment rating or load allocation needs review |
| Parent mismatch | Consumer list parent differs from SLD parent | Drawing and schedule disagree |
| SLD-only asset | Visible asset missing from consumer list | Possible missing database row or spare/future feeder |
| Consumer asset missing from SLD | Structured asset not visible in drawing | SLD may be incomplete or tag naming may differ |
| Voltage mismatch | Parent and child voltage levels differ | Hierarchy or voltage specification may be wrong |
| High VSD concentration | VSD share exceeds criteria | Harmonics/filtering assumptions may need review |
| Duplicate tag | Same `ITEM TAG` appears more than once | Traceability and aggregation risk |

## Demo Flow

| Step | User / System Action | Output |
|---|---|---|
| 1 | User uploads consumer list and SLD PDF | A review session is created |
| 2 | Backend runs the orchestrator | Intake, topology, calculation, and SLD agents execute |
| 3 | Gemini 2.5 Flash inspects the SLD PDF | Visible assets, parent tags, ratings, and confidence values |
| 4 | Python tools calculate and validate | Connected load, utilization, deterministic findings |
| 5 | Cross-checker compares visual SLD vs consumer graph | Missing assets, parent mismatches, voltage/rating differences |
| 6 | Dashboard renders results | KPIs, topology tree, issue cards, SLD preview |
| 7 | User opens report tab | Evidence-backed engineering report |

## Business Impact

For EPC companies, industrial plants, utilities, renewable developers, and engineering consultancies, document consistency is a real business problem. Design mismatches can trigger rework, procurement delays, site queries, and late engineering changes.

SingleLineIQ can help by:

- Reducing repetitive manual review time.
- Improving traceability between drawings and load lists.
- Finding inconsistencies earlier.
- Creating a clear issue database.
- Producing a first-pass engineering action report.
- Helping teams review synthetic or internal design data in a repeatable way.

## Current Scope

The MVP focuses on document consistency and connected-load review:

- One uploaded consumer list.
- One uploaded SLD PDF.
- Transformer, switchboard, MCC, panel, and final-load hierarchy.
- Recursive connected-load aggregation.
- Deterministic validation.
- Gemini-powered visual SLD extraction.
- Dashboard and report generation.

The app intentionally does not claim to replace full electrical studies. It is a design QA assistant, not a power-system simulation package.

## Future Work

Future versions could add:

- Revision-to-revision comparison.
- Automatic redline suggestions on the SLD.
- Cable schedule and protection device checks.
- Integration with ETAP, SKM, DIgSILENT, or other engineering tools.
- Long-term project memory for repeated design reviews.
- Human-in-the-loop issue approval before final reports.
- More robust CAD-native extraction from DXF or DWG-derived sources.

## Conclusion

SingleLineIQ demonstrates how agentic AI can support a real industrial engineering workflow. Gemini 2.5 Flash provides multimodal SLD understanding, specialized agents coordinate the review, Python tools perform deterministic calculations, and the Cloud Run app turns the result into an interactive dashboard and traceable engineering report.

The central idea is simple:

> The agent reads the drawing, maps the loads, checks the engineering logic, and gives the engineer a grounded action report.

This is not just document summarization. It is an agentic design-review workflow for electrical engineering document consistency.

# If you want to try out the app you can use the sample file in the following link

[Sample Files](https://github.com/jlgarciatucci/singlelineiq/tree/main/sample)
