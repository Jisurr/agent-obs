import pytest

from agent_obs.versioning.repository import VersionRepository

from .test_helpers import create_test_version



def test_get_latest_empty():
    """Test that get_latest returns None when the repository is empty."""
    repository = VersionRepository("agent-1")

    result = repository.get_latest()

    assert result is None
    
def test_get_latest_single_version():
    """Test that get_latest returns the only saved version."""
    repository = VersionRepository("agent-1")

    v1 = create_test_version("v1")
    repository.save(v1)

    result = repository.get_latest()

    assert result == v1
    
def test_get_latest_returns_most_recently_saved_version():
    """Test that get_latest returns the most recently saved version."""
    repository = VersionRepository("agent-1")

    v1 = create_test_version("v1")
    v2 = create_test_version("v2", "v1")
    v3 = create_test_version("v3", "v2")

    repository.save(v1)
    repository.save(v2)
    repository.save(v3)

    result = repository.get_latest()

    assert result == v3