"""Detects repeated cycles in multi-agent execution before budget is exhausted
(e.g. Agent A -> Tool -> Agent A -> Tool, repeated N times).
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core.trace import ExecutionGraph


@dataclass
class DetectedLoop:
    """A repeated structural cycle found in the execution graph."""

    cycle_node_ids: list[str]
    repeat_count: int


class LoopDetector:
    """Runs cycle detection over the causal graph to catch runaway
    agent-tool-agent loops early.
    """

    def __init__(self, graph: ExecutionGraph, min_repeats: int = 3):
        pass

    def detect(self) -> list[DetectedLoop]:
        """Return all detected repeated cycles above the configured threshold."""
        pass
