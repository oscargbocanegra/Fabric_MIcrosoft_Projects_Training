# Smart Device Analytics — Operations Runbook

## Pipeline sequence

| Stage | Fabric pipeline | Primary output |
|---|---|---|
| Ingestion | `pl_ingest_smart_device` | Bronze entities |
| Transformation | `pl_transformation_smart_device` | Silver entities |
| Processing | `pl_process_smart_device` | Coordinated end-to-end execution |
| Analysis | `pl_analize_smart_device` | Gold entities and Warehouse load |
| Reporting | `pl_report_smart_data` | Semantic model refresh |

## Standard operating procedure

1. Confirm the schedule, environment, source batch, and expected `file_date`.
2. Monitor the pipeline and retain the Fabric run identifier.
3. Validate record counts and DQ evidence after each layer.
4. Continue to the next stage only when the current stage passes its acceptance gate.
5. Confirm Warehouse reconciliation before refreshing the semantic model.
6. Record deviations, warnings, retries, and final outcome in the run evidence.

## Failure handling

| Symptom | First action | Recovery decision |
|---|---|---|
| Source folder/file not found | Confirm source availability and expected file pattern | Retry only after the source batch is complete |
| Notebook failure | Inspect activity output and preceding layer | Fix input/configuration; replay the smallest safe scope |
| Dataflow refresh failure | Inspect connection and transformation error | Correct connection or transformation, then rerun the affected dataflow |
| DQ `BLOCK` | Quarantine or stop promotion | Correct source/transformation; do not bypass the rule |
| Warehouse load failure | Check table state and stored-procedure parameters | Use full or incremental replay according to the affected `file_date` |
| Semantic refresh failure | Validate Warehouse availability and schema | Refresh after the Warehouse load is reconciled |
| Notification failure | Preserve the original pipeline failure | Use the monitoring channel; never add credentials to the notebook |

## Retry and idempotency

- Retry transient infrastructure failures only after confirming the target layer was not partially committed.
- For incremental loads, use the same `file_date` and verify that replay replaces the intended slice rather than appending duplicates.
- For full loads, validate that downstream consumers are stopped or isolated during replacement.
- Maximum automatic retries and backoff must be configured in the Fabric pipeline per environment; record the chosen values in the deployment evidence.

## Recovery targets

| Target | Initial project objective | Status |
|---|---:|---|
| RPO | One source batch (`file_date`) | Pending validation with business owner |
| RTO | 4 hours for a failed daily run | Initial engineering target |
| Evidence retention | 90 days minimum | Pending environment confirmation |

These are engineering targets for the lab, not production commitments. They must be validated before the project is labelled `Reference`.

## Escalation information

Every escalation must include environment, pipeline, activity, run ID, source batch/file date, affected entity, DQ result, error summary, and the last successful layer. Never include credentials, access tokens, or sensitive source records.

