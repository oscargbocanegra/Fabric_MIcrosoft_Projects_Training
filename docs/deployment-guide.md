# Smart Device Analytics — Deployment Guide

## Deployment principle

Deploy the project by environment. Artifact names and business contracts remain stable; workspace IDs, Lakehouse IDs/names, OneLake paths, connections, credentials, and notification targets are environment configuration and must not be copied as code between environments.

## Required services and permissions

| Capability | Minimum requirement |
|---|---|
| Fabric workspace | Capacity supporting Lakehouse, Warehouse, pipelines, Dataflows Gen2, notebooks, semantic model, and reports |
| Deployment identity | Permission to create/update artifacts and execute pipelines in the target workspace |
| Source access | Read access to the authorized smart-device source location |
| Secret management | Managed identity or approved secret store for source and notification credentials |
| Monitoring | Access to pipeline history, Dataflow refresh history, Warehouse query/load history, and semantic-model refresh history |

## Configuration checklist

- [ ] Target workspace selected for the environment.
- [ ] `lh_bronze`, `lh_silver`, and `lh_gold` assigned to the target workspace.
- [ ] Warehouse and semantic model connections mapped to target artifacts.
- [ ] Source locations and file patterns configured.
- [ ] Notebook default Lakehouse and OneLake paths parameterized.
- [ ] Dataflow Gen2 connections configured with managed credentials.
- [ ] Notification mechanism configured without embedded passwords or tokens.
- [ ] Pipeline parameters for full/incremental mode and `file_date` reviewed.
- [ ] DQ evidence destination and retention defined.

## Deployment sequence

1. Create or validate the workspace and capacity.
2. Deploy the three Lakehouses and validate their connections.
3. Deploy notebooks, Dataflows Gen2, and the Copy Job.
4. Deploy the Warehouse tables and stored procedures.
5. Deploy the semantic model and report.
6. Configure the five pipelines in dependency order: ingest, transformation, process, analysis, report.
7. Execute a controlled smoke test with a known source batch.
8. Run DQ validation and reconcile Bronze, Silver, Gold, and Warehouse counts.
9. Capture run evidence and approve promotion only when the acceptance gate passes.

## Promotion criteria

Promotion is accepted when the smoke test completes, DQ `BLOCK` rules pass, no secrets are present, target references resolve to the intended environment, and rollback inputs are available.

## Rollback

Stop downstream schedules, preserve the failed run ID, restore the prior artifact version or deployment snapshot, and replay only the affected batch after the root cause is corrected. Never delete source evidence to hide a failed deployment.

