"""Measures how a single agent's configuration change cascades through a
multi-agent system -- catching emergent effects that isolated per-agent
testing would miss.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CascadeImpact:
    """The effect of one agent's change on the rest of the system."""

    changed_agent: str
    affected_agents: list[str]
    unaffected_agents: list[str]
    latency_delta_pct: float
    cost_delta_pct: float


class CascadeAnalyzer:
    """Replays a multi-agent workflow with one agent's configuration changed,
    and reports which other agents' behavior shifted as a result.
    """

    def __init__(self, replay_engine):
        pass

    def analyze(self, changed_agent: str, new_configuration) -> CascadeImpact:
        """Run the cascade analysis for a single changed agent."""
        pass
