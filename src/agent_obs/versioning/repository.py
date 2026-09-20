from __future__ import annotations

from dataclasses import dataclass

from .artifact import AgentConfiguration
from .blame import FieldChange


@dataclass(frozen=True)
class Version:
    """A single committed snapshot of an agent configuration."""

    version_id: str
    parent_version_id: str | None
    configuration: AgentConfiguration
    author: str
    message: str
    created_at: float
    fingerprint: str


@dataclass
class ConfigurationDiff:
    """The set of field-level changes between two configuration versions."""

    version_a: str
    version_b: str
    changed_fields: dict[str, tuple[object, object]]


class VersionRepository:
    """Repository for storing and retrieving Version objects.

    The initial implementation uses in-memory storage and preserves
    version insertion order to support retrieval of the latest saved
    version.
    """

    """Git-like operations under agent-friendly naming.

    commit -> "save version", branch -> "experiment", tag -> "label",
    diff -> "configuration changes", revert -> "rollback".
    """

    def __init__(self, agent_id: str, storage=None):
        """Initialize the version repository.

        Args:
            agent_id (str): The unique identifier of the agent associated
                with this repository.
            storage (dict): The initial implementation
                uses in-memory storage.
        """
        self.agent_id = agent_id
        # Initial persistence strategy: in-memory storage.
        self._versions: dict[str, Version] = {}

    def save(self, version: Version):
        """Save a version in the in-memory repository.

        Args:
            version (Version): The Version object to store.

        Raises:
            ValueError: If the version ID already exists or the specified
                parent version does not exist.
        """
        if not self.check_version(version):
            raise ValueError(
                f"Version '{version.version_id}' already exists "
            )

        self._versions[version.version_id] = version

    def get(self, version_id: str) -> Version:
        """Retrieve a version by its ID.

        Args:
            version_id (str): The unique identifier of the version to retrieve.

        Returns:
            The Version associated with the given ID.

        Raises:
            KeyError: If no version with the given ID exists.
        """
        return self._versions[version_id]

    def list_versions(self) -> list[Version]:
        """Return all versions in their save order.

        Returns:
            A list containing all versions stored in the repository,
            ordered from oldest saved version to newest.
        """
        return list(self._versions.values())

    def get_latest(self) -> Version | None:
        """Return the most recently saved version.

        Returns:
            The latest Version according to save order, or None if the
            repository contains no versions.
        """
        if not self._versions:
            return None
        else:
            return list(self._versions.values())[-1]

    def check_version(self, version: Version) -> bool:
        """Validate whether a version can be saved.

        Args:
            version (Version): The Version object to validate.

        Returns:
            True if the version can be saved, otherwise False.
        """
        if version.version_id in self._versions:
            return False

        return True