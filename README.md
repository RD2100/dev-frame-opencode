# Dev-Frame OpenCode

**Agent Runtime Governance Monorepo** — evidence-first, GPT-reviewed, fail-closed pipeline for AI-assisted software engineering.

## Status

[![Smoke](https://img.shields.io/badge/smoke-5%2F5%20PASS-brightgreen)](smoke_report.txt)
[![Tests](https://img.shields.io/badge/tests-748%20passed-brightgreen)](smoke_report.txt)
[![Production](https://img.shields.io/badge/production-promoted-blue)](CURRENT_ROUTE.json)

```
production_promotion_approved: true
broader_real_chain_testing_unblocked: true
hardcoded_driver_replacement_approved: true
Smoke: 5/5 PASS | Tests: 748 (532 core + 216 e2e)
```

## Projects

| Project | Path | Description |
|---------|------|-------------|
| **codegraph** | `codegraph/` | Local-first code intelligence (tree-sitter), CLI, and MCP server for AI agent code exploration |
| **ai-workflow-hub** | `ai-workflow-hub/` | OpenCode-driven coding automation — 4-node pipeline (human_gate, executor, tester, fixer) with SADP TaskSpec support |
| **ai-workflow-hub-e2e** | `ai-workflow-hub-e2e/` | End-to-end evidence integrity and gate tests — API integration, watchdog, model validation, SHA256 signing |

## Architecture

```
codegraph (MCP readiness) → ai-workflow-hub (core state machine) → ai-workflow-hub-e2e (evidence integrity)
```

## Quick Start

```bash
# Verify all projects
python smoke_test.py

# Individual checks
cd codegraph && npx tsc --noEmit          # TypeScript type-check
cd ai-workflow-hub && python -m pytest tests/ -v   # 532 core tests
cd ai-workflow-hub-e2e && python -m pytest tests/ -v # 216 e2e tests
```

## Governance Model

- **Evidence-First**: every claim requires verifiable evidence in ZIP packs
- **Fail-Closed**: review_unverified, RID mismatch, CDP unavailable → stop
- **GPT as Review Authority**: all authorizations flow through GPT-reviewed evidence packs
- **Append-Only Evidence**: no deletion, movement, or renaming of historical evidence
- **Staged Unblocking**: blocked items are unlocked through sequential P0-P15 pipeline

## Guard System

10/10 submit scripts guarded via `tools/submission_guard.py`:
- `pre_submit_gate()` — dedup, cooldown, max 3 retries
- `record_submission_result()` — append-only JSONL logging, fail-closed
- `check_before_submit()` — pre-flight submission check
- `record_submission()` — low-level log writer
- `get_submission_summary()` — diagnostic aggregator

## Requirements

- Python >= 3.10
- Node.js >= 20.0.0
- `codegraph/node_modules/` installed (`npm ci`)
- `ai-workflow-hub` dependencies (`pip install -e ".[dev]"`)
- `ai-workflow-hub-e2e` dependencies (`pip install -e .`)

## License

MIT
