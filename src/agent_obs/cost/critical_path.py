"""Identifies the chain of calls that actually determines end-to-end latency
(e.g. three 300ms parallel searches cost 310ms total, not 890ms), the way
distributed tracing tools compute a critical path.
"""

from __future__ import annotations

from ..core.trace import ExecutionGraph


class CriticalPathAnalyzer:
    """Computes the critical path through an execution graph, accounting for
    parallel branches.
    """

    def __init__(self, graph: ExecutionGraph):
        pass

    def critical_path(self) -> list[str]:
        """Return the ordered node ids that make up the critical (blocking) path."""
        pass

    def total_latency_ms(self) -> float:
        """Wall-clock latency implied by the critical path, not the sum of all nodes."""
        pass
