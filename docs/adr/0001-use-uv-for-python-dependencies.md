# 0001 — Use uv for Python dependencies

- **Status:** Accepted
- **Date:** 2026-05-07
- **Deciders:** Backend foundation plan

## Context

The website is maintained long-term by rotating IEEE student board members.
Onboarding speed matters more than tool maturity: someone cloning the repo
for the first time should be running the API within minutes, not fighting
virtualenvs or stale lockfiles.

The realistic options are pip + requirements.txt, Poetry, and uv.

## Decision

Use **[uv](https://docs.astral.sh/uv/)** as the dependency manager and
virtualenv driver. Commit `uv.lock`. All `make` targets invoke Python
through `uv run` so contributors never need to remember whether their
venv is activated.

## Consequences

- Positive: a single static binary; `uv sync` installs everything in
  seconds; no "did you `source .venv/bin/activate`?" failures.
- Positive: lockfile is reproducible across CI and dev machines.
- Negative / accepted cost: uv is younger than Poetry; some students may
  not have heard of it. The README and Makefile remove most reasons to
  care about that distinction.
- Follow-up: pin uv version in CI (`astral-sh/setup-uv@v3` with
  `version: "0.5.x"`) so a breaking uv release doesn't break our pipeline.

## Alternatives considered

- **pip + requirements.txt** — no resolver, no lockfile semantics worth
  the name, deps drift.
- **Poetry** — more familiar but slower, and `poetry install` is slow
  enough that contributors notice on every `make install`.
- **PDM, Hatch (env management)** — fewer users, no clear upside over uv.
