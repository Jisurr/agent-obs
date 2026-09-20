"""Tracks reads/writes to shared memory across agents, so corruption or
staleness can be traced back to the responsible agent.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MemoryAccess:
    """A single read or write to a shared memory key."""

    key: str
    agent: str
    operation: str  # "read" | "write"
    timestamp: float
    value: object = None


class SharedMemoryTracker:
    """Records every access to shared memory keys during a run."""

    def __init__(self):
        pass

    def record_access(self, access: MemoryAccess) -> None:
        """Log a memory read or write."""
        pass

    def history_for(self, key: str) -> list[MemoryAccess]:
        """Return the full read/write history for a single memory key."""
        pass
