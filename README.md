# Microsoft Fabric Projects Training

> A governed, living catalog of hands-on Microsoft Fabric projects for data engineering, analytics, data governance, and applied AI.

[![Microsoft Fabric](https://img.shields.io/badge/Microsoft-Fabric-0078D4?logo=microsoft&logoColor=white)](https://learn.microsoft.com/fabric/)
[![Architecture](https://img.shields.io/badge/Architecture-Lakehouse%20Medallion-5B2C6F)](#working-principles)
[![Catalog](https://img.shields.io/badge/Catalog-Governed-107C10)](#project-catalog)

## Purpose

This repository is the governed entry point for reusable Microsoft Fabric learning and reference projects. Each project develops an end-to-end capability: data ingestion, transformation, quality controls, semantic modeling, visualization, and operational documentation.

`main` is the portfolio catalog and common governance baseline. Project implementation lives in its own `project/<project-name>` branch.

## Working principles

| Principle | Application |
|---|---|
| Reproducibility | Fabric artifacts are stored as versionable code and configuration. |
| Layered architecture | Raw, standardized, and consumption data are separated through Bronze, Silver, and Gold layers. |
| Quality and traceability | Data contracts, validation evidence, and execution traceability are part of delivery. |
| Governance by design | Naming, documentation, security, and semantic modeling are addressed from the beginning. |
| Business value | Every project must answer a clear analytical or operational question. |
| Progressive maturity | Projects start as working labs and evolve through controlled hardening. |

## Project catalog

| Project | Status | Scope | Branch |
|---|---|---|---|
| Wind Turbine Power Analysis | In progress | Daily ingestion, Medallion Lakehouse, semantic model, and wind-generation analytics. | [Open project](../../tree/project/wind_turbine_power_analysis) |
| Smart Device Analytics | Hardening | Smart-device catalog ingestion, standardization, Warehouse, semantic model, and executive reporting. | [Open project](../../tree/project/SmartDeviceAnaliticsWS) |

### Maturity status

| Status | Meaning |
|---|---|
| Planned | The scope has been defined but no functional implementation is published. |
| In progress | The project is being implemented or validated as a lab. |
| Hardening | The functional solution exists; portability, security, data quality, and operational controls are being strengthened. |
| Reference | The project meets the agreed governance and operational acceptance criteria. |

## Minimum governance baseline

Before a project is labelled **Reference**, it must provide:

- A project README in English describing its purpose, architecture, prerequisites, deployment, operations, and known risks.
- No embedded secrets, passwords, environment-specific IDs, or non-portable OneLake paths in versioned artifacts.
- A documented data contract, executable or evidenced data-quality checks, and a runbook.
- Architecture decisions (ADRs) for material design choices.
- A repeatable validation process, including secret scanning and artifact/static checks where applicable.
- Pull-request-based changes to the project branch, with the catalog updated when project scope or status changes.

## Branch model

```text
main                              # Living catalog, common standards, and portfolio documentation
project/<project-name>            # Self-contained project implementation
feature/<project>-<capability>    # Scoped project enhancement
fix/<project>-<issue>             # Scoped corrective change
```

Changes are reviewed into their `project/...` branch. `main` is updated only for cross-cutting standards, catalog entries, or project maturity changes.

## How to use this repository

1. Use this catalog to identify a project and its maturity status.
2. Open the project branch and read its README before deploying artifacts.
3. Clone the selected branch, for example:

   ```bash
   git clone --branch project/SmartDeviceAnaliticsWS \
     https://github.com/oscargbocanegra/Fabric_MIcrosoft_Projects_Training.git
   ```

4. Deploy or synchronize artifacts to an authorized Microsoft Fabric workspace.
5. Record design decisions, validation evidence, and operating changes with the project.

## Technology scope

Microsoft Fabric · OneLake · Lakehouse · Python Notebooks · SQL · Data Pipelines · Dataflows Gen2 · Warehouse · Power BI · Semantic Models · Medallion Architecture · Data Quality · Automation · Generative AI

## Scope statement

This is a learning and technical experimentation repository. Projects prioritize reusable engineering patterns, governance practices, and verifiable evidence before enterprise adoption.
