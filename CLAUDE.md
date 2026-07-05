# CLAUDE.md — Mac_AI_Onboarding_Toolkit

Project rules for this repo. Global rules in `~/.claude/CLAUDE.md` still apply — this
file only adds project specifics. Committed to git.

## What this repo is
A living boilerplate reference: one numbered sub-folder per AI framework/tool, each a
working, documented, reusable starting point. Also the hands-on curriculum for Phase 5.

## Objective (the What)
Make every folder a copy-paste-ready foundation for real projects, so future work starts
from a known-good, current (July 2026) setup instead of a blank page.

## Philosophy (the Why)
- WHY before HOW; always compare alternatives and state switching cost.
- Optimize for no lock-in (OpenAI-compatible escape hatches, provider-swappable layers).
- Size every local-model choice to 24 GB RAM.
- Skim first, deep-dive only on explicit request. Don't pre-build a folder's code unless asked.

## Structure & conventions
- Folders `01_…` → `18_…`. Each is self-contained: own `.venv`, own `.env`.
- Setup in any folder:
  - `cd <folder>`
  - `uv init`
  - `uv python pin 3.12`
  - `uv add <packages from that folder's README>`
  - `cp ../.env.example .env`
- Run: `uv run python <file>.py`  (never bare `python`)
- Python 3.12 always (never 3.13). Use `uv`, never raw `pip`/`pyenv`/system Python.
- Secrets: copy from `.env.example`; never commit `.env`. Never modify `.gitignore_global`.
- Tests in `tests/`, use `pytest`.
- API testing: Bruno collections (`.bru`) beside the code. Never Postman.

## Framework selection (decision engine)
Before choosing a framework for a task, consult `compatibility_matrix.md` in this repo.
It maps need → folder and lists switching costs. Reach for the lowest layer that works;
add LangChain/LangGraph/CrewAI only when raw SDK calls get tangled.

## Repo hygiene
- pre-commit: `uv tool install pre-commit` then `pre-commit install` (config in `.pre-commit-config.yaml`).
- Reproduce toolchain: `brew bundle --file=Brewfile`.
- Keep `data/`, `models/`, `chroma_db/`, `.venv/` out of git (already in `.gitignore`).

## Status
Scaffold + per-folder instructions complete. Each folder marked ⬜ (scaffold) or ✅
(tooling installed). Deep-dives fill in runnable `example.py` per folder on request.
Next: 5·2 Anthropic SDK.
