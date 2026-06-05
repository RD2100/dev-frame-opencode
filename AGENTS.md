# AGENTS.md — dev-frame-opencode / agent-acceptance

> Generated: 2026-06-05 | Git: master
> Status: PRODUCTION PROMOTED

## 项目状态

**PRODUCTION PROMOTED** — 3/5 blocked items 已授权解锁，2 个永久保护。

## 已完成 Goals（全部 GPT accepted）

| # | Goal | 状态 |
|---|------|------|
| 1 | bounded guarded review pipeline | CLOSED |
| 2 | Claude/Codex interchangeable peer orchestrators | ACCEPTED |
| 3 | limited broader real-chain execution (680 tests: 464 core + 216 e2e) | ACCEPTED |
| 4 | Runbook/Monitoring/Ledger hardening | ACCEPTED |
| 5 | Production Readiness Preparation | ACCEPTED |
| 6 | Goal Execution Automation Hardening | ACCEPTED |
| 7 | Claude Continuity Hardening | ACCEPTED |

## Blocked Items（仅剩 2 个永久保护）

```json
{
  "production_promotion_approved": true,
  "broader_real_chain_testing_unblocked": true,
  "hardcoded_driver_replacement_approved": true,
  "guard_removal_approved": false,
  "evidence_cleanup_approved": false
}
```

## 关键文件

| 文件 | 用途 |
|------|------|
| RUNBOOK.md | 操作系统规范 |
| PROJECT_STATE.md | 项目状态 |
| CURRENT_ROUTE.json | 当前路由（所有 blocked false） |
| DECISION_LEDGER.jsonl | 关键决策记录 |
| TRANSITION_LOG.jsonl | 阶段流转日志 |
| HEALTH_REPORT.md | 健康报告 |
| FAILURE_MODE_MATRIX.md | 失败模式矩阵 |
| PRODUCTION_READINESS_CHECKLIST.md | 生产准备检查清单 |
| PRODUCTION_RISK_MATRIX.md | 生产风险矩阵 |
| ROLLBACK_PLAN.md | 回滚计划 |
| MONITORING_PLAN.md | 监控计划 |
| RELEASE_CRITERIA.md | 发布条件 |
| HUMAN_OVERRIDE_PROTOCOL.md | 人工介入协议 |
| FAILURE_RESPONSE_RUNBOOK.md | 失败响应手册 |
| PRODUCTION_READINESS_GAPS.md | 生产准备差距 |
| PRODUCTION_READINESS_SUMMARY.md | 生产准备总结 |
| tools/AUTHORIZED_GPT_CONVERSATION.json | 授权 GPT 对话绑定 |
| tools/gpt_conversation_guard.py | GPT 对话授权 guard |

## 操作规范（RUNBOOK.md 规则）

1. **脚本文件**: 多步骤阶段必须使用 `tools/_*.py` 脚本文件，禁止长 inline bash
2. **自动轮询**: CDP 提交后 60s 延迟，最多 3 次重试，验证 exact REVIEW_RUN_ID
3. **自动链式**: accepted review → persist → verify POST_REVIEW_ROUTE → auto-chain
4. **标准流水线**: authorize → execute → submit → poll → persist → chain/close
5. **停止规则**: review_unverified / blocked / human_required / RID mismatch → stop

## 下一步建议

1. Guard Policy Reassessment（P16，guard_removal 仍 blocked）
2. Evidence Archive Maintenance（P17，evidence_cleanup 仍 blocked）
3. Broader Real-Chain Full Testing（已解锁，可扩展）

## 证据目录

```
_reports/conversation-authorization/
  claude-continuity-hardening-probe-v1/          # 连续性验证完成
  production-readiness-preparation-execution-v1/ # 生产准备完成
  runbook-monitoring-ledger-hardening-execution-v1/ # 文档巩固完成
  limited-broader-real-chain-execution-v1/       # 限执行完成
```
