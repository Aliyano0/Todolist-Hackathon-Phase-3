"""Pytest configuration and fixtures."""

import pytest
from adapters.repository.memory_repository import MemoryRepository
from src.core.ports.repository import Repository


@pytest.fixture
def repository() -> Repository:
    """Provide a fresh MemoryRepository instance for each test."""
    return MemoryRepository()


@pytest.fixture(autouse=True)
def reset_shared_repository() -> None:
    """Reset the shared CLI repository before each test.

    This ensures tests don't affect each other's state when using the CLI.
    The shared repository in adapters.cli.__main__ is used for session persistence.
    """
    from adapters.cli import __main__
    __main__._repository = MemoryRepository()
