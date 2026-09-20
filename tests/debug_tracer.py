from agent_obs.tracing.tracer import Tracer
from agent_obs.core.enums import NodeType


class DummyBackend:
    def __init__(self):
        self.nodes = []

    def save_node(self, node):
        self.nodes.append(node)


backend = DummyBackend()
tracer = Tracer(backend=backend)

print("Backend:", tracer.backend)
print("Has save_node:", hasattr(tracer.backend, "save_node"))

with tracer.span(NodeType.AGENT) as node:
    node.set_output("test")

print("Nodes:", len(backend.nodes))
print("Output:", backend.nodes[0].output_data)