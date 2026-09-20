from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from .enums import NodeType


@dataclass
class TraceNode:
    """
    Role:
        Represents a single atomic unit of agent execution.

    Type:
        Classifies each step using NodeType (e.g., LLM_CALL, TOOL_CALL).

    When & Why:
        Instantiated and tracked during workflow execution to capture 
        comprehensive telemetry, inputs, outputs, latency, and cost per step.

    Exception Tracking:
        Records runtime errors and exceptions natively to enable robust 
        debugging, root-cause analysis, and system auditing.

    Output:
        Exposes a raw telemetry data structure ready for serialization 
        and persistence.
    """

    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    node_type: NodeType = NodeType.LLM_CALL
    parent_id: str | None = None
    timestamp: float = field(default_factory=time.time)
    prompt_hash: str | None = None
    model: str | None = None
    temperature: float | None = None
    seed: int | None = None
    latency_ms: float | None = None
    cost_usd: float | None = None
    input_data: Any = None
    output_data: Any = None
    memory_snapshot: dict | None = None
    tool_parameters: dict | None = None
    tool_result: Any = None
    exception: str | None = None
    retry_count: int = 0
    tags: list[str] = field(default_factory=list)

    def set_output(self, output):
        """
        Role:
            Stores the resulting data produced by this execution step.

        When & Why:
            Called upon successful completion of an operation (e.g., LLM text output 
            or tool result) to capture and persist the final output payload.

        Output:
            Updates the internal `output_data` field of the node.
        """
        self.output_data = output

    def to_dict(self) -> dict[str, Any]:
        """
        Role:
            Converts the TraceNode instance and its internal attributes 
            into a standard, flat Python dictionary format.

        When & Why:
            Invoked before serialization, local file persistence, or JSON logging, 
            allowing complex dataclass objects to safely cross system boundaries 
            and be stored or transmitted.

        Output:
            Returns a `dict[str, Any]` containing all node fields, with enums 
            properly unwrapped to their primitive string values.
        """
        return {
            "node_id": self.node_id,
            "node_type": (
                self.node_type.value
                if isinstance(self.node_type, NodeType)
                else self.node_type
            ),
            "parent_id": self.parent_id,
            "timestamp": self.timestamp,
            "prompt_hash": self.prompt_hash,
            "model": self.model,
            "temperature": self.temperature,
            "seed": self.seed,
            "latency_ms": self.latency_ms,
            "cost_usd": self.cost_usd,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "memory_snapshot": self.memory_snapshot,
            "tool_parameters": self.tool_parameters,
            "tool_result": self.tool_result,
            "exception": self.exception,
            "retry_count": self.retry_count,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TraceNode:
        """
        Role:
            Reconstructs and instantiates a TraceNode object from a stored dictionary.

        When & Why:
            Invoked when loading serialized logs, reading execution history from local 
            files, or restoring a graph for offline debugging and analysis, safely 
            converting primitive values back into their expected types.

        Output:
            Returns a fully typed, ready-to-use `TraceNode` instance with all its 
            telemetry fields and unwrapped enums restored.
        """
        data_copy = data.copy()
        if "node_type" in data_copy and isinstance(data_copy["node_type"], str):
            data_copy["node_type"] = NodeType(data_copy["node_type"])
        return cls(**data_copy)

    def finish_trace(self, latency_ms: float | None = None) -> None:
        """
        Role:
            Finalizes the lifespan of the node and tracks execution duration.

        When & Why:
            Invoked at the end of a step to measure performance. If explicit 
            latency is provided, it uses it; otherwise, it computes the exact 
            elapsed time in milliseconds from the node's creation timestamp.

        Output:
            Updates the internal `latency_ms` field with the total execution time.
        """
        if latency_ms is not None:
            self.latency_ms = latency_ms
        else:
            self.latency_ms = (time.time() - self.timestamp) * 1000

    def set_exception(self, exc):
        """
        Role:
            Captures, formats, and stores runtime errors and exceptions.

        When & Why:
            Triggered automatically when an unexpected error or failure occurs 
            during a workflow step, ensuring the exception type and message 
            are safely recorded for root-cause analysis and debugging.

        Output:
            Updates the internal `exception` field with a formatted string 
            containing both the error name and its message.
        """
        error_name = type(exc).__name__
        error_message = str(exc)
        self.exception = error_name + ": " + error_message