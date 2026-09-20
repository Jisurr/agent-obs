"""Tracks shared prompt components (e.g. a reusable tool description) across
many agents, so editing one shared piece immediately shows every agent it
silently affects instead of leaving that discovery to production incidents.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ComponentChange:
    """A version bump of one shared prompt component."""

    component_id: str
    old_version: str
    new_version: str


class LineageTracker:
    """Maps shared components to every artifact/agent that references them."""

    def __init__(self, storage=None):
        pass

    def register_component(self, component_id: str, content: str) -> str:
        """Register or update a shared component, returning its new version."""
        pass

    def affected_agents(self, component_id: str) -> list[str]:
        """Return every agent whose compiled artifact includes this component."""
        pass
