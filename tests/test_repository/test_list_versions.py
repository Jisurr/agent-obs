import pytest

from agent_obs.versioning.repository import VersionRepository

from .test_helpers import create_test_version


def test_list_versions_empty():
    """Test that listing an empty repository returns an empty list."""
    repository = VersionRepository("agent-1")

    result = repository.list_versions()

    assert result == []
    
    
def test_list_versions():
    """Test that listing the repository returns saved versions."""
    repository = VersionRepository("agent-1")

    version = create_test_version("v1")
    repository.save(version)

    result = repository.list_versions()

    assert result == [version]
    
    
def test_list_versions_preserves_save_order():
    """Test that versions are returned in their save order."""
    repository = VersionRepository("agent-1")

    v1 = create_test_version("v1")
    v2 = create_test_version("v2", "v1")
    v3 = create_test_version("v3", "v2")

    repository.save(v1)
    repository.save(v2)
    repository.save(v3)

    result = repository.list_versions()

    assert result == [v1, v2, v3]