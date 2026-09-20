import pytest

from agent_obs.versioning.repository import VersionRepository

from .test_helpers import create_test_version


def test_save_version():
    """Test that a valid version can be saved to the repository."""
    repository = VersionRepository("agent-1")

    version = create_test_version("v1")

    repository.save(version)

    assert repository.get("v1") == version


def test_save_duplicate_version():
    """Test that saving a version with an existing ID raises ValueError."""
    repository = VersionRepository("agent-1")

    version = create_test_version("v1")

    repository.save(version)

    with pytest.raises(ValueError):
        repository.save(version)

