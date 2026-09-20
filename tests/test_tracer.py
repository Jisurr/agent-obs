import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure project root is in Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent_obs.core.enums import NodeType
from agent_obs.tracing.tracer import Tracer


@pytest.fixture
def mock_backend():
    """Provides a mock storage backend for assertions."""
    backend = MagicMock()
    backend.save_node = MagicMock()
    return backend


@pytest.fixture
def tracer_instance(mock_backend):
    """Provides a Tracer instance configured with a mock backend."""
    return Tracer(backend=mock_backend)


def test_trace_agent_execution_flow(tracer_instance, mock_backend):
    """Test that @trace_agent creates a root node and persists it."""

    @tracer_instance.trace_agent
    def run_agent(query: str):
        return f"Processed: {query}"

    result = run_agent("Test Query")

    assert result == "Processed: Test Query"
    assert mock_backend.save_node.call_count == 1

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.node_type == NodeType.AGENT
    assert saved_node.parent_id is None
    assert saved_node.latency_ms >= 0

    graph = tracer_instance.get_graph()

    assert saved_node.node_id in graph.nodes
    assert graph.root_node_id == saved_node.node_id


def test_trace_tool_call_metadata(tracer_instance, mock_backend):
    """Test tool parameters, result, output, and node type."""

    @tracer_instance.trace_tool_call
    def multiply(a: int, b: int = 2):
        return a * b

    result = multiply(5, b=3)

    assert result == 15
    assert mock_backend.save_node.call_count == 1

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.node_type == NodeType.TOOL_CALL

    tool_params = saved_node.tool_parameters

    assert tool_params["a"] == 5
    assert tool_params["b"] == 3

    assert saved_node.tool_result == 15
    assert saved_node.output_data == 15
    assert saved_node.latency_ms >= 0


def test_trace_llm_call_metadata_extraction(
    tracer_instance,
    mock_backend,
):
    """Test extracting model and temperature from decorator and kwargs."""

    @tracer_instance.trace_llm_call(model="gpt-4o-mini")
    def generate_text(
        prompt: str,
        temperature: float = 0.7,
    ):
        return "Generated response"

    result = generate_text(
        "Hello",
        temperature=0.2,
    )

    assert result == "Generated response"
    assert mock_backend.save_node.call_count == 1

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.node_type == NodeType.LLM_CALL
    assert saved_node.model == "gpt-4o-mini"
    assert saved_node.temperature == 0.2
    assert saved_node.output_data == "Generated response"
    assert saved_node.latency_ms >= 0


def test_nested_execution_tree(
    tracer_instance,
    mock_backend,
):
    """Test automatic parent-child relationships."""

    @tracer_instance.trace_tool_call
    def fetch_data(item_id: str):
        return f"Item {item_id}"

    @tracer_instance.trace_llm_call
    def summarize(text: str):
        return f"Summary of {text}"

    @tracer_instance.trace_agent
    def agent_workflow(item_id: str):
        data = fetch_data(item_id)
        summary = summarize(data)
        return summary

    result = agent_workflow("123")

    assert result == "Summary of Item 123"
    assert mock_backend.save_node.call_count == 3

    saved_nodes = [
        call[0][0]
        for call in mock_backend.save_node.call_args_list
    ]

    tool_node = saved_nodes[0]
    llm_node = saved_nodes[1]
    agent_node = saved_nodes[2]

    assert tool_node.node_type == NodeType.TOOL_CALL
    assert llm_node.node_type == NodeType.LLM_CALL
    assert agent_node.node_type == NodeType.AGENT

    assert agent_node.parent_id is None
    assert tool_node.parent_id == agent_node.node_id
    assert llm_node.parent_id == agent_node.node_id

    graph = tracer_instance.get_graph()

    assert len(graph.nodes) == 3
    assert agent_node.node_id in graph.nodes
    assert tool_node.node_id in graph.nodes
    assert llm_node.node_id in graph.nodes

    assert graph.root_node_id == agent_node.node_id

    children = graph.children(agent_node.node_id)
    child_ids = {node.node_id for node in children}

    assert tool_node.node_id in child_ids
    assert llm_node.node_id in child_ids

    graph.validate_consistency()


def test_exception_handling(
    tracer_instance,
    mock_backend,
):
    """Test that exceptions are recorded and re-raised."""

    @tracer_instance.trace_tool_call
    def failing_tool():
        raise ValueError("Database connection failed")

    with pytest.raises(
        ValueError,
        match="Database connection failed",
    ):
        failing_tool()

    assert mock_backend.save_node.call_count == 1

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.exception is not None
    assert "ValueError" in saved_node.exception
    assert "Database connection failed" in saved_node.exception
    assert saved_node.latency_ms >= 0


def test_tool_exception_is_not_swallowed(
    tracer_instance,
    mock_backend,
):
    """Test that the original tool exception reaches the caller."""

    @tracer_instance.trace_tool_call
    def divide_by_zero():
        return 10 / 0

    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    assert mock_backend.save_node.call_count == 1

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.exception is not None
    assert "ZeroDivisionError" in saved_node.exception


def test_llm_runtime_parameters(
    tracer_instance,
    mock_backend,
):
    """Test that LLM parameters can be captured from runtime kwargs."""

    @tracer_instance.trace_llm_call
    def call_llm(
        prompt: str,
        model: str = "default-model",
        temperature: float = 0.5,
        seed: int = 42,
    ):
        return "response"

    result = call_llm(
        "Hello",
        model="test-model",
        temperature=0.3,
        seed=123,
    )

    assert result == "response"

    saved_node = mock_backend.save_node.call_args[0][0]

    assert saved_node.node_type == NodeType.LLM_CALL
    assert saved_node.model == "test-model"
    assert saved_node.temperature == 0.3
    assert saved_node.seed == 123


def test_graph_serialization(tracer_instance):
    """Test that the execution graph can be serialized and restored."""

    @tracer_instance.trace_agent
    def run_agent():
        return "done"

    run_agent()

    graph = tracer_instance.get_graph()

    data = graph.to_dict()

    assert data["run_id"] == graph.run_id
    assert len(data["nodes"]) == 1

    restored_graph = type(graph).from_dict(data)

    assert restored_graph.run_id == graph.run_id
    assert len(restored_graph.nodes) == len(graph.nodes)
    assert restored_graph.root_node_id == graph.root_node_id


def test_multiple_independent_executions(
    tracer_instance,
    mock_backend,
):
    """Test that separate top-level calls create separate root nodes."""

    @tracer_instance.trace_tool_call
    def tool(value):
        return value * 2

    first_result = tool(5)
    second_result = tool(10)

    assert first_result == 10
    assert second_result == 20

    assert mock_backend.save_node.call_count == 2

    graph = tracer_instance.get_graph()

    assert len(graph.nodes) == 2

    saved_nodes = [
        call[0][0]
        for call in mock_backend.save_node.call_args_list
    ]

    assert saved_nodes[0].parent_id is None
    assert saved_nodes[1].parent_id is None