"""Attributes cost down the execution graph, node by node and subtree by
subtree, so "run cost: $0.14" becomes "where did the money go".
"""

from __future__ import annotations

from dataclasses import dataclass

from ..core.trace import ExecutionGraph


@dataclass
class CostBreakdown:
    """Cost attributed to a single node."""

    node_id: str
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    tool_cost_usd: float = 0.0
    embedding_cost_usd: float = 0.0
    storage_cost_usd: float = 0.0

    @property
    def total_usd(self) -> float:
        """Total cost for this node alone."""
        pass


class CostAttributor:
    """Walks an ExecutionGraph and attributes cost per node and per subtree."""

    def __init__(self, graph: ExecutionGraph, pricing: dict | None = None):
        pass

    def breakdown_for(self, node_id: str) -> CostBreakdown:
        """Cost breakdown for a single node."""
        pass

    def subtree_total(self, node_id: str) -> float:
        """Total cost of a node and everything it caused."""
        pass

    def cost_per_success(self, success_predicate) -> float:
        """Total cost divided by the number of runs satisfying success_predicate."""
        pass
