import os

import pytest

from mcp_testrail.testrail_client import TestRailClient


@pytest.fixture
def mock_testrail_client():
    """Fixture providing a TestRailClient with mocked httpx requests."""
    return TestRailClient(
        base_url="http://example.testrail.io",
        username="test@example.com",
        api_key="test_api_key",
    )


@pytest.fixture
def testrail_client():
    """
    Fixture providing a real TestRailClient for integration tests.

    Requires environment variables:
    - TESTRAIL_URL
    - TESTRAIL_USERNAME
    - TESTRAIL_API_KEY
    """
    base_url = os.getenv("TESTRAIL_URL")
    username = os.getenv("TESTRAIL_USERNAME")
    api_key = os.getenv("TESTRAIL_API_KEY")

    if not all([base_url, username, api_key]):
        pytest.skip(
            "Real TestRail credentials not provided. Set TESTRAIL_URL, TESTRAIL_USERNAME, and TESTRAIL_API_KEY environment variables."
        )

    return TestRailClient(
        base_url=base_url,
        username=username,
        api_key=api_key,
    )


@pytest.fixture
def test_project_name():
    return "Document AI"
