
"""Execution context propagated through a single agent run."""

from __future__ import annotations
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionContext:
    run_id: str
    graph: Any
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self._node_stack: ContextVar[list] = ContextVar(
            f"trace_stack_{self.run_id}",
            default=[],
        )

    def get_current_node(self):
        stack = self._node_stack.get()
        return stack[-1] if stack else None

    def push_node(self, node):
        stack = self._node_stack.get().copy()
        current = self.get_current_node()

        if current is not None and node.parent_id is None:
            node.parent_id = current.node_id

        stack.append(node)
        self._node_stack.set(stack)

    def pop_node(self):
        stack = self._node_stack.get().copy()

        if stack:
            stack.pop()

        self._node_stack.set(stack)

    def clear(self):
        self._node_stack.set([])

    def child_context(self, **metadata):
        return ExecutionContext(
            run_id=self.run_id,
            graph=self.graph,
            metadata={
                **self.metadata,
                **metadata,
            },
        )