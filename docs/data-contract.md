# Smart Device Analytics — Data Contract

## Contract purpose

This contract defines the minimum interface between source files, the Medallion layers, the Warehouse, and downstream consumers. A load is accepted only when the rules below are satisfied or an approved exception is recorded.

## Contract metadata

| Field | Value |
|---|---|
| Contract ID | `SDA-DATA-001` |
| Owner | Smart Device Analytics project team |
| Scope | Device catalog and technical characteristics |
| Grain | One record per business entity key and source load |
| Source format | Authorized source files discovered by `pl_ingest_smart_device` |
| Landing layer | `lh_bronze` |
| Standardized layer | `lh_silver` |
| Consumption layer | `lh_gold`, `wh_smart_device` |
| Change policy | Additive changes require compatibility review; breaking changes require an ADR and version increment |

## Entities and keys

| Entity | Business key | Required relationships |
|---|---|---|
| `device` | `device_id` | References `model_id`, category and technical dimensions as applicable |
| `model` | `model_id` | References `brand_id` and `category_id` |
| `category` | `category_id` | Parent for model classification |
| `brand` | `brand_id` | Parent for model classification |
| `camera` | `camera_id` | Technical attribute associated with a device/model |
| `connectivity` | `connectivity_id` | Technical attribute associated with a device/model |
| `operating_system` | `operating_system_id` | Technical attribute associated with a device/model |
| `display` | `display_id` | Technical attribute associated with a device/model |
| `physical_specs` | `physical_specs_id` | Technical attribute associated with a device/model |
| `dim_time` | `date_key` | Calendar dimension for analytical reporting |
| `fact_device` | Device fact grain defined by the Warehouse model | References all applicable dimensions |

The exact column names and types are defined by the source and Fabric artifacts at deployment time. Any change to a key, relationship, nullability, unit, or grain is a breaking change until reviewed.

## Layer responsibilities

| Layer | Responsibility | Acceptance condition |
|---|---|---|
| Bronze | Preserve source content and load metadata with minimal transformation | Source files are traceable to a load and no silent overwrite occurs |
| Silver | Normalize names, types, domains, units, and relationships | DQ rules pass or the run is quarantined |
| Gold | Publish analytical entities and business-ready grain | Keys and relationships are stable for consumers |
| Warehouse | Serve relational consumption and load procedures | Full/incremental load is repeatable and reconciled |
| Semantic model | Expose governed measures and relationships | Refresh succeeds after Warehouse validation |

## Load metadata

Each accepted load must make the following information available in the operational evidence:

- `run_id` or Fabric pipeline run identifier.
- `source_file` or source batch identifier.
- `file_date` when supplied by the source.
- `ingestion_timestamp`.
- `environment`.
- Records received, accepted, rejected, and written per entity.
- DQ result and exception reference.

## Contract failure policy

1. Stop promotion to the next layer when a critical key, schema, or referential rule fails.
2. Preserve the failed input and execution identifier for investigation.
3. Record the failure in the run evidence; do not hide it through a forced retry.
4. Resume only after the source or transformation is corrected and the affected scope is replayable.

