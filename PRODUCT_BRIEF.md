# SingleLineIQ Product Brief

SingleLineIQ is an agentic electrical single-line reviewer.

The system reviews a plant electrical design by reading a full-hierarchy consumer list, inferring the electrical topology from parent-child relationships, calculating downstream loads, visually inspecting a CAD-exported single-line diagram PDF, and generating an engineering review.

The consumer list is the structured source of truth.

The SLD PDF is an independent visual cross-check.

The MVP uses synthetic anonymized data only.

## Core capabilities

- Infer topology from `ITEM TAG` and `PARENT ITEM TAG`.
- Represent transformers, switchboards, MCCs, DBs, and final loads as graph nodes.
- Calculate downstream connected load by panel, switchboard, transformer, and main board.
- Detect overloaded panels and transformers.
- Detect duplicate tags and missing ratings.
- Detect invalid parent-child relationships.
- Extract visible assets from SLD PDF using Gemini vision or fallback extract.
- Compare inferred topology against the visual SLD.
- Generate traceable findings and a professional report.

## Non-goals

The system must not claim to perform load flow, short-circuit, arc flash, protection coordination, motor-starting, or full power-system studies.
