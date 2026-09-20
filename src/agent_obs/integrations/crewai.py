"""Auto-instrumentation for CrewAI crews and agents."""

from __future__ import annotations

from ..tracing.tracer import Tracer


class CrewAIInstrumentor:
    """Attaches a Tracer to a CrewAI crew so multi-agent runs are traced
    without manual decoration.
    """

    def __init__(self, tracer: Tracer):
        pass

    def instrument(self, crew) -> None:
        """Attach tracing hooks to a CrewAI crew."""
        pass
