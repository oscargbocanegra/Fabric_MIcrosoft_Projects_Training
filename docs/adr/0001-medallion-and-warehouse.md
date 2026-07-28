# ADR-0001: Medallion layers with Warehouse consumption

- Status: Accepted
- Date: 2026-07-27
- Scope: Smart Device Analytics

## Context

The solution ingests multiple smart-device entities, applies standardization, and exposes analytical results through a semantic model and report. A single storage layer would mix source preservation, transformations, and consumer-facing structures.

## Decision

Use Bronze, Silver, and Gold Lakehouses, followed by `wh_smart_device` for relational consumption. Pipelines coordinate the transitions, and the semantic model reads the governed analytical result.

## Consequences

- Source data can be preserved and replayed from Bronze.
- Standardization is isolated in Silver.
- Gold and Warehouse provide stable consumption contracts.
- Each layer requires explicit reconciliation and DQ evidence.
- Additional storage and orchestration increase operational responsibility.

