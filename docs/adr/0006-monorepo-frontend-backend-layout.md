# 0006 — Monorepo for frontend and backend

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

The frontend (Nuxt 4) and the backend (FastAPI) could live in separate
repositories or share one. The team is small, the codebases are coupled
at the API contract, and the people working on them rotate every year.

## Decision

Single repository. Top-level layout:

```
website/
  frontend/          # Nuxt 4 app
  backend/           # FastAPI service
  docs/adr/          # decision records (this file)
  .github/workflows/ # per-stack CI workflows
  .husky/, .pre-commit-config.yaml, commitlint.config.mjs   # shared quality gates
```

CI workflows are **path-filtered**: changes under `frontend/**` only run
the frontend job; `backend/**` only runs the backend job. Pre-commit
hooks use file-type filters so frontend and backend tooling don't
interfere.

## Consequences

- Positive: a single PR can change the API contract on both sides
  atomically. No "deploy backend, wait, deploy frontend" dance for
  small changes.
- Positive: shared commit conventions, license, and ADR location.
- Positive: one clone, one IDE workspace.
- Negative / accepted cost: contributors see code from a stack they
  don't work on. Path filters and per-stack READMEs keep this contained.
- Follow-up: if the project ever grows to multiple deployable
  backends, revisit. Not a near-term concern.

## Alternatives considered

- **Two repos** — more discipline around versioning the API contract,
  but a heavier PR workflow for a 2–4 person team.
- **Polyrepo with shared "contracts" repo** — overkill at this scale.
