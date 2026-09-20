"""Registries mapping actions to their compensating (rollback) counterparts.

Keeping this mapping declarative and separate from the action implementations
means error-handling logic never has to be embedded in ordinary tool code.
"""

from __future__ import annotations

from collections.abc import Callable


class ActionRegistry:
    """Registers primary actions (tools/operations) available to the agent."""

    def __init__(self):
        pass

    def register(self, name: str, func: Callable) -> None:
        """Register an action under a name."""
        pass

    def get(self, name: str) -> Callable:
        """Look up a registered action."""
        pass


class CompensationRegistry:
    """Maps each action name to its compensating (rollback) action."""

    def __init__(self):
        pass

    def register(self, action_name: str, compensation: Callable) -> None:
        """Register the compensation for a given action."""
        pass

    def get(self, action_name: str) -> Callable | None:
        """Look up the compensation for an action, if any."""
        pass
