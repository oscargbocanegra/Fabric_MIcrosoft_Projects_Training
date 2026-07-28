# Smart Device Analytics — Value Demonstration

## Purpose

This document defines how the laboratory demonstrates technical and analytical value without presenting unverified production claims. Structural metrics are observed from the repository; runtime metrics must be captured from a Fabric execution.

## Demonstration storyline

1. Start with the smart-device source entities and identify the business questions.
2. Run ingestion into Bronze and show the source batch and `file_date`.
3. Run transformation into Silver and show standardized entities and DQ results.
4. Run processing into Gold and the Warehouse, reconciling input and output counts.
5. Refresh the semantic model and open the report to demonstrate consumer access.
6. Replay one batch to demonstrate deterministic processing and duplicate control.

## Evidence matrix

| Capability | Evidence to capture | Acceptance criterion | Status |
|---|---|---|---|
| Ingestion | Pipeline run ID, source batch, records received/written | Bronze load completes and is traceable to the batch | Pending runtime capture |
| Standardization | Silver table preview and DQ result by rule ID | All `BLOCK` rules pass or an exception is recorded | Pending runtime capture |
| Analytical model | Gold/Warehouse count reconciliation | Accepted records reconcile across layers | Pending runtime capture |
| Repeatability | Two runs with the same `file_date` | No unexpected duplicate business keys | Pending runtime capture |
| Reporting | Power BI report screenshot and refresh run | Report opens with refreshed semantic-model data | Pending runtime capture |
| Learning value | README, docs, and editable diagram | A reviewer can follow the lab without private context | Available in repository |

## Repository-observed baseline

| Metric | Value | Interpretation |
|---|---:|---|
| Source entities | 9 | Device catalog and technical dimensions are represented. |
| Notebooks | 18 | Ingestion, transformation, shared utilities, and notification flow. |
| Data Pipelines | 5 | Ingestion, transformation, processing, analysis, and reporting stages. |
| Dataflows Gen2 | 4 | Declarative transformations for selected dimensions. |
| Lakehouses | 3 | Bronze, Silver, and Gold separation. |
| Warehouse / semantic model / report | 1 / 1 / 1 | Relational and visual consumption path. |
| Report pages / visuals | 1 / 13 | A compact executive summary surface is versioned. |

These values describe versioned artifacts, not processed row counts, latency, freshness, or business impact.

## Runtime evidence template

Copy this block into the project notes after a successful Fabric run:

```text
Execution date (UTC):
Environment:
Source batch / file_date:
Pipeline run IDs:
Records received:
Records accepted:
Records rejected:
Bronze records:
Silver records:
Gold records:
Warehouse records:
DQ result: PASS / WARN / BLOCK
Semantic-model refresh: PASS / FAIL
Report screenshot path or URL:
Replay result:
Known deviation and remediation:
```

## Lab acceptance gate

The demonstration is complete when the reviewer can see:

- One successful end-to-end run with retained identifiers.
- One DQ result linked to the documented rule IDs.
- One reconciliation from Bronze through Warehouse.
- One report screenshot showing the analytical output.
- One replay result for the same `file_date`.
- No claims based only on repository structure are labelled as runtime or business outcomes.

## Scope note

This is a learning laboratory. Security controls and production hardening are outside this P1 demonstration scope; the focus is portfolio coherence, reproducibility, data flow, and visible analytical value.
