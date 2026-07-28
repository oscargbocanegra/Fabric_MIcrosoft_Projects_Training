# ADR-0002: Incremental Warehouse load by `file_date`

- Status: Accepted
- Date: 2026-07-27
- Scope: `sp_incremental_load` and analysis pipeline

## Context

The project receives source batches identified by `file_date`. Reloading a batch must not append duplicate records to the Warehouse.

## Decision

Use `file_date` as the incremental replay boundary. The incremental procedure removes the target slice for the requested date and inserts the corresponding source slice. A full load remains available for controlled rebuilds.

## Consequences

- A batch can be replayed deterministically when the source is unchanged.
- The process depends on consistent `file_date` values and safe parameter handling.
- Reconciliation must verify counts and duplicate business keys after every replay.
- Full-load execution requires a maintenance window or consumer isolation.

