# Smart Device Analytics — Data Quality Rules

## Rule policy

Rules are evaluated by entity and load. `BLOCK` prevents promotion; `WARN` allows promotion only when the exception is documented. The implementation may run in notebooks, Dataflows Gen2, Warehouse SQL, or a dedicated validation step, but the rule IDs and thresholds are stable contract identifiers.

## Minimum rule set

| ID | Dimension | Scope | Rule | Severity | Threshold |
|---|---|---|---|---|---|
| DQ-001 | Schema | Every entity | Required columns exist with the expected type | BLOCK | 100% |
| DQ-002 | Completeness | All business keys | Business key is not null or blank | BLOCK | 100% |
| DQ-003 | Uniqueness | `device`, `model`, `category`, `brand` | Business key is unique within the accepted batch | BLOCK | 100% |
| DQ-004 | Referential integrity | Dimensions and `fact_device` | Every foreign key resolves to its parent dimension | BLOCK | 100% |
| DQ-005 | Domain conformity | Categorical attributes | Value belongs to the approved domain or is explicitly `unknown` | BLOCK | 100% |
| DQ-006 | Numeric validity | Display and physical specifications | Numeric values are parseable and non-negative where the attribute requires it | BLOCK | 100% |
| DQ-007 | Format conformity | Dates and identifiers | Dates use the declared format; identifiers contain no control characters | BLOCK | 100% |
| DQ-008 | Completeness | Required descriptive attributes | Required-field completion is at least 98% per entity | WARN/BLOCK | Project owner decides exception; default BLOCK for keys |
| DQ-009 | Volume anomaly | Every entity | Accepted volume is within 50%–200% of the previous comparable load, unless a full load is declared | WARN | 50%–200% |
| DQ-010 | Freshness | Every run | Latest source/load timestamp is within the agreed processing window | BLOCK | Define target SLA per environment |
| DQ-011 | Reconciliation | Bronze to Silver/Gold | Written records equal accepted records minus documented rejects | BLOCK | 100% reconciliation |
| DQ-012 | Idempotency | Incremental Warehouse load | Replaying the same `file_date` does not create duplicate business keys | BLOCK | 0 unexpected duplicates |

## Execution evidence

For every run, publish a compact result with:

| Field | Description |
|---|---|
| `run_id` | Fabric pipeline execution identifier |
| `rule_id` | Rule evaluated |
| `entity` | Table or dataflow output |
| `status` | `PASS`, `WARN`, or `BLOCK` |
| `input_count` / `output_count` | Reconciliation counts |
| `failed_count` | Records failing the rule |
| `executed_at` | UTC execution timestamp |
| `exception_ref` | Link or identifier for approved exception, when applicable |

## Acceptance gate

The processing pipeline may advance from Bronze to Silver and from Silver to Gold only when all `BLOCK` rules pass. A `WARN` result requires an owner, rationale, expiry date, and remediation reference.

