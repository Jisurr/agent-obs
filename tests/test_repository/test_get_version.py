import pytest

from agent_obs.versioning.repository import VersionRepository

from .test_helpers import create_test_version


def test_get_existing_version():
    """Test that an existing version can be retrieved by its ID."""
    repository = VersionRepository("agent-1")

    version = create_test_version("v1")
    repository.save(version)

    result = repository.get("v1")

    assert result == version
    
    
def test_get_nonexistent_version():
    """Test that getting a nonexistent version raises KeyError."""
    repository = VersionRepository("agent-1")

    with pytest.raises(KeyError):
        repository.get("does-not-exist")