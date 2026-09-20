"""Auto-instrumentation for LangChain agents and chains."""

from __future__ import annotations

from ..tracing.tracer import Tracer


class LangChainInstrumentor:
    """Attaches a Tracer to LangChain callbacks so chains/agents are traced
    without manual decoration.
    """

    def __init__(self, tracer: Tracer):
        pass

    def instrument(self, chain_or_agent) -> None:
        """Attach tracing callbacks to a LangChain object."""
        pass
