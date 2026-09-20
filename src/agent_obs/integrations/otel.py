"""Exports execution graphs as standard OpenTelemetry spans."""

from __future__ import annotations

from ..core.trace import ExecutionGraph


class OtelExporter:
    """Translates an ExecutionGraph into OTel spans so runs show up in
    existing observability stacks (Datadog, Grafana, Honeycomb, etc.)
    instead of requiring a bespoke dashboard.
    """

    def __init__(self, endpoint: str | None = None):
        pass

    def export(self, graph: ExecutionGraph) -> None:
        """Export a completed graph as OTel spans."""
        pass
