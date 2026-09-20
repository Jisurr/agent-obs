"""Field-level change history -- 'git blame' for a single configuration field."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FieldChange:
    """One historical change to a single configuration field."""

    version_id: str
    field_path: str
    old_value: object
    new_value: object
    author: str
    changed_at: float
    reason: str | None = None


class BlameIndex:
    """Indexes field-level changes across a version history for fast blame lookups."""

    def __init__(self, repository):
        pass

    def history_for(self, field_path: str) -> list[FieldChange]:
        """Return the ordered change history for a single field."""
        pass
