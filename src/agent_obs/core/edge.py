from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import EdgeType


@dataclass
class TraceEdge:
    """
    Role:
        Represents a directed connection (edge) establishing a causal or logical link between two trace nodes.

    Type:
        Classifies the relationship using EdgeType (e.g., PARENT_CHILD, TOOL_CALL, DELEGATED_TO).

    When & Why:
        Instantiated whenever two steps or components are connected in the workflow, 
        allowing the system to map execution flow, dependencies, and data movement.

    Output:
        Exposes a clean structure linking source and target nodes with custom metadata, ready for graph assembly.
    """

    source_id: str
    target_id: str
    edge_type: EdgeType = EdgeType.PARENT_CHILD
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Role:
            Converts the TraceEdge instance and its attributes into a standard dictionary.

        When & Why:
            Invoked before serialization, file persistence, or graph export, ensuring 
            enums are unwrapped for safe JSON storage.

        Output:
            Returns a `dict[str, Any]` containing the source ID, target ID, unwrapped edge type, and metadata.
        """
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": (
                self.edge_type.value
                if isinstance(self.edge_type, EdgeType)
                else self.edge_type
            ),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TraceEdge:
        """
        Role:
            Reconstructs and instantiates a TraceEdge object from a stored dictionary.

        When & Why:
            Invoked when loading saved graphs from local files or logs, safely converting 
            serialized string values back into their proper `EdgeType` enums.

        Output:
            Returns a fully typed `TraceEdge` instance ready for graph reconstruction.
        """
        data_copy = data.copy()
        if "edge_type" in data_copy and isinstance(data_copy["edge_type"], str):
            data_copy["edge_type"] = EdgeType(data_copy["edge_type"])
        return cls(**data_copy)
