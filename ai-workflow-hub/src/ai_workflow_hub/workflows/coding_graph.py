"""LangGraph 工作流定义 — OpenCode-only 编码闭环 (5 节点).

节点: human_gate -> execute -> test -> fix/final
路由: test passes -> final, test fails & rounds < max -> fix, fails & rounds >= max -> final
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from ..schemas import WorkflowState
from ..nodes.executor import executor_node
from ..nodes.tester import tester_node
from ..nodes.fixer import fixer_node
from ..nodes.human_gate import human_gate_node
from ..nodes.finalizer import finalizer_node


def create_coding_graph(checkpointer: MemorySaver | None = None) -> StateGraph:
    """创建编码工作流状态图 (带 checkpointer).

    状态机结构:

    start
      |
    human_gate_node         [入口 — 接收 TaskSpec]
      |
    execute_node             [调用 OpenCode 执行代码修改]
      |
    test_node                [每个 fix 轮后重新执行]
      |
    (test route)
      |-- passed -> final_node
      |-- fail + round < max -> fix_node -> test_node
      |-- fail + round >= max -> final_node
    """

    graph = StateGraph(WorkflowState)

    # 添加节点
    graph.add_node("human_gate_node", _wrap(human_gate_node))
    graph.add_node("execute_node", _wrap_with_guard(executor_node, "execute_node"))
    graph.add_node("test_node", _wrap(tester_node))
    graph.add_node("fix_node", _wrap_with_guard(fixer_node, "fix_node"))
    graph.add_node("final_node", _wrap(finalizer_node))

    # 入口: human_gate
    graph.set_entry_point("human_gate_node")

    # human_gate -> execute (或 END 如果需要人工)
    graph.add_conditional_edges(
        "human_gate_node",
        _human_gate_route,
        {
            "execute_node": "execute_node",
            "__end__": END,
        },
    )

    # execute -> test
    graph.add_edge("execute_node", "test_node")

    # test -> route_decision
    graph.add_conditional_edges(
        "test_node",
        _test_route,
        {
            "fix_node": "fix_node",
            "final_node": "final_node",
        },
    )

    # fix -> test
    graph.add_edge("fix_node", "test_node")

    # final -> END
    graph.add_edge("final_node", END)

    return graph


def compile_graph(thread_id: str) -> Any:
    """编译带 MemorySaver checkpointer 的图（单进程内存模式，不跨进程持久化）.

    Args:
        thread_id: run_id，映射为 LangGraph thread_id
    """
    checkpointer = MemorySaver()
    graph = create_coding_graph(checkpointer)
    return graph.compile(checkpointer=checkpointer)


def _s(state: dict[str, Any] | Any) -> dict[str, Any]:
    """安全解包 state: WorkflowState -> dict."""
    if hasattr(state, "model_dump"):
        return state.model_dump()
    if isinstance(state, dict):
        return state
    return {}


def _human_gate_route(state: dict[str, Any] | Any) -> str:
    """human_gate 后路由: 如果需要人工 -> END, 否则继续 execute."""
    s = _s(state)
    if s.get("human_required", False) or s.get("status") == "human_required":
        return "__end__"
    return "execute_node"


def _test_route(state: dict[str, Any] | Any) -> str:
    """test 后路由: test 通过 -> final, 失败但有 round 剩余 -> fix, 失败无 round -> final."""
    s = _s(state)
    test_passed = s.get("test_exit_code", -1) == 0
    if test_passed:
        return "final_node"

    fix_round = s.get("fix_round", 0)
    max_fix_rounds = s.get("max_fix_rounds", 3)
    if fix_round < max_fix_rounds:
        return "fix_node"

    return "final_node"


def _wrap(fn):
    """Wrap node function — 兼容 dict / WorkflowState / Pydantic model."""
    def wrapped(state: dict[str, Any] | WorkflowState | Any) -> dict[str, Any]:
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        elif isinstance(state, dict):
            state_dict = state
        else:
            state_dict = dict(state) if state else {}
        result = fn(state_dict)
        # 先更新非 backend_calls 字段，再合并 backend_calls
        bc = result.pop("backend_calls", None)
        state_dict.update(result)
        if bc:
            state_dict.setdefault("backend_calls", {}).update(bc)
        return state_dict
    return wrapped


def _wrap_with_guard(fn, node_name: str):
    """Wrap 副作用节点 (execute_node, fix_node).

    execute_node: 恢复时已执行则跳过，避免重复调用 OpenCode。
    fix_node: 按轮次允许重复: fix_node:0, fix_node:1, ...
    """

    def guarded(state: dict[str, Any] | WorkflowState | Any) -> dict[str, Any]:
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        elif isinstance(state, dict):
            state_dict = state
        else:
            state_dict = dict(state) if state else {}

        executed = set(state_dict.get("executed_nodes", []))
        side_effect = state_dict.get("side_effect_nodes", ["execute_node", "fix_node"])

        if node_name not in side_effect:
            pass
        elif node_name == "fix_node":
            round_key = f"{node_name}:{state_dict.get('fix_round', 0)}"
            if round_key in executed:
                state_dict.setdefault("execution_log", "")
                state_dict["execution_log"] += f"\n[SKIPPED] {round_key} already executed (resumed from checkpoint)\n"
                return state_dict
        elif node_name in executed:
            state_dict.setdefault("execution_log", "")
            state_dict["execution_log"] += f"\n[SKIPPED] {node_name} already executed (resumed from checkpoint)\n"
            return state_dict

        # 正常执行
        result = fn(state_dict)
        bc = result.pop("backend_calls", None)
        state_dict.update(result)
        if bc:
            state_dict.setdefault("backend_calls", {}).update(bc)

        # 标记已执行
        executed_list = list(state_dict.get("executed_nodes", []))
        if node_name == "fix_node":
            mark = f"{node_name}:{state_dict.get('fix_round', 0)}"
        else:
            mark = node_name
        if mark not in executed_list:
            executed_list.append(mark)
        state_dict["executed_nodes"] = executed_list

        return state_dict

    return guarded
