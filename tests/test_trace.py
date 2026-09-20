from agent_obs.tracing.tracer import Tracer
from agent_obs.core.node import TraceNode
from agent_obs.core.enums import NodeType


class DummyBackend:
    def __init__(self):
        self.nodes = []

    def save_node(self, node):
        self.nodes.append(node)


def test_trace_node_methods():
    node = TraceNode(node_type=NodeType.LLM_CALL)

    node.set_output("Test Output")

    assert node.output_data == "Test Output"

    node.finish_trace()

    assert node.latency_ms is not None

    try:
        raise ValueError("Test Error")
    except Exception as e:
        node.set_exception(e)

    assert "ValueError: Test Error" in node.exception


def test_execution_context_stack():
    tracer = Tracer()
    context = tracer.context

    assert context.get_current_node() is None

    node1 = TraceNode(node_type=NodeType.AGENT)

    context.push_node(node1)

    assert context.get_current_node() == node1

    node2 = TraceNode(node_type=NodeType.LLM_CALL)

    context.push_node(node2)

    assert context.get_current_node() == node2

    context.pop_node()

    assert context.get_current_node() == node1

    context.pop_node()

    assert context.get_current_node() is None


def test_tracer_span_basic_flow():
    backend = DummyBackend()
    tracer = Tracer(backend=backend)

    with tracer.span(NodeType.AGENT) as node:
        node.set_output("Agent result")

    assert node.output_data == "Agent result"
    assert node.node_type == NodeType.AGENT
    assert node.latency_ms is not None

    assert len(backend.nodes) == 1
    assert backend.nodes[0] == node

    assert tracer.context.get_current_node() is None


def test_tracer_span_nested_parent_child():
    backend = DummyBackend()
    tracer = Tracer(backend=backend)

    with tracer.span(NodeType.AGENT) as parent:
        assert tracer.context.get_current_node() == parent

        with tracer.span(NodeType.TOOL_CALL) as tool:
            assert tracer.context.get_current_node() == tool

            with tracer.span(NodeType.LLM_CALL) as llm:
                assert tracer.context.get_current_node() == llm

    assert len(backend.nodes) == 3

    assert tool.parent_id == parent.node_id
    assert llm.parent_id == tool.node_id

    assert tracer.context.get_current_node() is None


def test_tracer_span_exception_handling():
    backend = DummyBackend()
    tracer = Tracer(backend=backend)

    try:
        with tracer.span(NodeType.LLM_CALL) as node:
            raise RuntimeError("LLM API Rate Limit Exceeded")
    except RuntimeError:
        pass

    assert len(backend.nodes) == 1

    failed_node = backend.nodes[0]

    assert failed_node.exception is not None
    assert "RuntimeError: LLM API Rate Limit Exceeded" in failed_node.exception

    assert failed_node.latency_ms is not None
    assert failed_node.latency_ms >= 0

    assert tracer.context.get_current_node() is None


def test_tracer_trace_named_span():
    backend = DummyBackend()
    tracer = Tracer(backend=backend)

    with tracer.trace("my_agent", NodeType.AGENT) as node:
        node.set_output("Agent finished")

    assert len(backend.nodes) == 1

    saved_node = backend.nodes[0]

    assert saved_node.node_type == NodeType.AGENT
    assert saved_node.output_data == "Agent finished"
    assert "my_agent" in saved_node.tags

    assert tracer.context.get_current_node() is None


def test_tracer_metadata():
    backend = DummyBackend()
    tracer = Tracer(backend=backend)

    with tracer.span(
        NodeType.LLM_CALL,
        model="gpt-4",
        temperature=0.7,
        seed=42,
        cost_usd=0.005,
        tags=["production", "test"],
    ) as node:

        node.input_data = {"prompt": "Hello"}
        node.set_output({"response": "World"})

    assert len(backend.nodes) == 1

    saved_node = backend.nodes[0]

    assert saved_node.model == "gpt-4"
    assert saved_node.temperature == 0.7
    assert saved_node.seed == 42
    assert saved_node.cost_usd == 0.005

    assert "production" in saved_node.tags
    assert "test" in saved_node.tags

    assert saved_node.input_data["prompt"] == "Hello"
    assert saved_node.output_data["response"] == "World"


def test_tracer_without_backend():
    tracer = Tracer()

    with tracer.span(NodeType.AGENT) as node:
        node.set_output("No backend")

    assert node.output_data == "No backend"
    assert node.latency_ms is not None

    assert tracer.context.get_current_node() is None