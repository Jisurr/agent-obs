import uuid

from agent_obs.versioning.artifact import AgentConfiguration, PromptArtifact
from agent_obs.versioning.extractor import AgentConfigurationExtractor
from agent_obs.versioning.repository import VersionRepository
from agent_obs.versioning.service import VersioningService
from tests.test_helpers import make_configuration
from agent_obs.versioning.fingerprint import FingerprintComputer


def test_commit_creates_first_version():
    """Verify that committing the first configuration creates a root version with no parent."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Initial configuration",
    )

    assert version.parent_version_id is None
    assert version.configuration == configuration
    assert version.author == "Khalil"
    assert version.message == "Initial configuration"
    assert version.fingerprint == FingerprintComputer.compute(configuration)
    assert version.version_id in repository._versions


def test_commit_uses_latest_version_as_parent():
    """Verify that a new commit uses the latest existing version as its parent."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    first_configuration = make_configuration()

    first_version = service.commit(
        configuration=first_configuration,
        author="Khalil",
        message="Initial configuration",
    )

    second_configuration = AgentConfiguration(
        prompt=PromptArtifact(
                system_prompt="You are an expert SQL assistant.",
                model="GPT-5",
                model_parameters={
                    "temperature": 0.2,
                    "top_p": 1.0,
                    "max_tokens": 500,
                },
            )
    )

    second_version = service.commit(
        configuration=second_configuration,
        author="Khalil",
        message="Improve SQL instructions",
    )

    assert second_version.parent_version_id == first_version.version_id


def test_commit_stores_and_returns_version():
    """Verify that the committed version is stored in the repository and returned by commit."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Initial configuration",
    )

    stored_version = repository.get(version.version_id)

    assert stored_version is version


def test_commit_generates_unique_version_id():
    """Verify that each committed version receives a valid UUID version identifier."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Initial configuration",
    )

    parsed_version_id = uuid.UUID(version.version_id)

    assert str(parsed_version_id) == version.version_id


def test_commit_sets_created_at_with_millisecond_precision():
    """Verify that the committed version timestamp is stored as a float with millisecond precision."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Initial configuration",
    )

    assert isinstance(version.created_at, float)
    assert version.created_at == round(version.created_at, 3)


def test_committing_same_configuration_twice_creates_distinct_versions():
    """Verify that identical configurations can be committed as distinct versions with different IDs."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    first_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="First save",
    )

    second_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Second save",
    )

    assert first_version.fingerprint == second_version.fingerprint
    assert first_version.version_id != second_version.version_id
    assert second_version.parent_version_id == first_version.version_id


def test_commit_reflects_configuration_change_in_fingerprint():
    """Verify that committing a changed configuration produces a different fingerprint."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    first_configuration = make_configuration()

    first_version = service.commit(
        configuration=first_configuration,
        author="Khalil",
        message="Initial configuration",
    )

    second_configuration = AgentConfiguration(
        prompt=PromptArtifact(
            system_prompt="You are an expert SQL assistant.",
            model="GPT-5",
            model_parameters={
                "temperature": 0.7,
                
            },
        )
    )

    second_version = service.commit(
        configuration=second_configuration,
        author="Khalil",
        message="Improve instructions",
    )

    assert first_version.fingerprint != second_version.fingerprint


def test_commit_builds_continuous_parent_chain():
    """Verify that successive commits form a continuous parent chain in commit order."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    first_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 1",
    )

    second_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 2",
    )

    third_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 3",
    )

    assert first_version.parent_version_id is None
    assert second_version.parent_version_id == first_version.version_id
    assert third_version.parent_version_id == second_version.version_id


def test_commit_preserves_author_and_message():
    """Verify that commit preserves the author and message metadata on the created version."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="alice",
        message="Tune temperature for SQL generation",
    )

    assert version.author == "alice"
    assert version.message == "Tune temperature for SQL generation"


def test_commit_keeps_all_versions():
    """Verify that committing multiple versions keeps every version available in the repository."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    first_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 1",
    )

    second_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 2",
    )

    third_version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Version 3",
    )

    versions = repository.list_versions()

    assert len(versions) == 3
    assert versions == [
        first_version,
        second_version,
        third_version,
    ]


def test_committed_version_keeps_original_configuration_values():
    """Verify that a committed version retains its original configuration values after the source is modified."""

    repository = VersionRepository(agent_id="agent-1")
    service = VersioningService(repository)
    configuration = make_configuration()

    version = service.commit(
        configuration=configuration,
        author="Khalil",
        message="Initial configuration",
    )

    original_fingerprint = version.fingerprint

    configuration.prompt.model_parameters["temperature"] == 0.9

    assert version.configuration.prompt.model_parameters["temperature"]== 0.2
    assert version.fingerprint == original_fingerprint


def test_empty_repository_has_no_latest_version():
    """Verify that a repository with no committed versions returns None as its latest version."""

    repository = VersionRepository(agent_id="agent-1")

    assert repository.get_latest() is None
