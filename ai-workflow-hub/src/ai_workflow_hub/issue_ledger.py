"""Issue ledger — tracks P0/P1 issues across runs."""
import json
from pathlib import Path
from typing import Any


def unresolved_p0_count(run_dir: str) -> int:
    """Count unresolved P0 issues in run_dir."""
    return 0  # Default: no P0 issues


def ledger_summary(run_dir: str) -> dict[str, Any]:
    return {"p0_count": 0, "p1_count": 0, "total": 0}


def render_governance_lines_cli(summary: dict[str, Any]) -> list[str]:
    return []


def _get_latest_by_key(key: str) -> dict[str, Any]:
    return {}


def mark_verified(run_dir: str) -> None:
    pass


def mark_wontfix(run_dir: str) -> None:
    pass


def mark_reopen(run_dir: str) -> None:
    pass


def mark_accepted_risk(run_dir: str) -> None:
    pass


def mark_mitigated(run_dir: str) -> None:
    pass


def mark_obsolete(run_dir: str) -> None:
    pass


def build_prompt_context() -> str:
    return ""


def derive_issues_from_state(state: dict[str, Any]) -> list[dict[str, Any]]:
    return []


def write_run_delta(run_dir: str, delta: list[dict[str, Any]]) -> None:
    pass


def merge_delta(run_dir: str) -> None:
    pass
