# ADR-0003: Externalize environment-specific configuration

- Status: Proposed
- Date: 2026-07-27
- Scope: notebooks, pipelines, Dataflows Gen2, and notifications

## Context

The current project artifacts include environment-dependent Lakehouse references and OneLake paths. Promoting those values across workspaces is not portable and can direct processing to the wrong environment.

## Decision

Move workspace IDs, Lakehouse references, OneLake paths, connection references, source locations, and notification targets into deployment parameters or approved environment configuration. Credentials must be resolved through managed identity or an external secret store.

## Acceptance criteria

- No environment-specific IDs or paths are required to be edited inside business logic.
- Development and production deployments resolve different target references from configuration.
- A deployment validation confirms that all references belong to the target workspace.
- Notification code contains no password, token, or SMTP secret.

