# AGENTS.md -- dev-frame-opencode

> Canonical root: D:\dev-frame-opencode
> Phase: M1 完成，M2 待定义
> Runtime: RD2100 Agent Runtime v2 (D:\agent-acceptance)
> Generated: 2026-05-30

## Quick Start

1. [CLAUDE.md](CLAUDE.md) -- 项目概述、健康状态、烟雾测试
2. [smoke_report.txt](smoke_report.txt) -- 最新烟雾测试报告
3. Memory: `C:\Users\RD\.claude\projects\D--dev-frame-opencode\memory\`

## Sub-Projects

| 项目 | 路径 | 验证 |
|------|------|------|
| codegraph | `codegraph/` | `npx tsc --noEmit` |
| ai-workflow-hub | `ai-workflow-hub/` | `pytest tests/` (77) |
| ai-workflow-hub-e2e | `ai-workflow-hub-e2e/` | `pytest tests/fittrack/ tests/test_gate.py tests/test_sha256.py` (175) |

## Development Process: SADP

This project uses the [Sub-Agent Dispatch Protocol](D:\agent-acceptance\docs\agent-runtime\sub-agent-dispatch-protocol.md):

- **@go [description]**: Create TaskSpec → dispatch → execute → ExecutionReport
- **@next**: Evaluate gate, generate next TaskSpec
- **@done**: Mark complete, prompt next goal
- **@review**: Output Reviewer Index

## Hard Stops (P0)

| # | Rule | Source |
|---|------|--------|
| 1 | No destructive git without human approval | RD2100 core-001 |
| 2 | No secrets in code, logs, or reports | RD2100 sec-001 |
| 3 | No command injection or path traversal | RD2100 sec-002, sec-003 |
| 4 | No fake green (FAILED/BLOCKED != PASS) | RD2100 review-001 |
| 5 | No write outside approved scope | RD2100 core-005 |
| 6 | Verify with `python smoke_test.py` before declaring health | project-local |

## Document Map

```
.aiworkflow/session/current.json      <- Current session state
memory/                                <- Project memory (persistent)
docs/                                  <- PRD, MVP plan, process log
CLAUDE.md                              <- Project overview + governance history
smoke_test.py                          <- Cross-project smoke runner
smoke_report.txt                       <- Latest smoke output
```

## Runtime Governance

RD2100 Agent Runtime is active at `D:\agent-acceptance\`. The governance hook
(`pre-edit.governance.ps1`) fires globally via `settings.json`.

Full rules: `D:\agent-acceptance\docs\agent-runtime\`
Capability inventory: `D:\agent-acceptance\docs\agent-runtime\capability-inventory.md`
