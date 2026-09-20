"""Visualizes and queries the message-passing graph between agents."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentMessage:
    """A single message exchanged between two agents."""

    sender: str
    recipient: str
    content: str
    timestamp: float


class CommunicationGraph:
    """Builds a queryable graph of agent-to-agent communication for a run."""

    def __init__(self):
        pass

    def record(self, message: AgentMessage) -> None:
        """Record a message exchange."""
        pass

    def conversation_between(self, agent_a: str, agent_b: str) -> list[AgentMessage]:
        """Return all messages exchanged between two specific agents."""
        pass
