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


@pytest.fixture
def new_test_case(testrail_client: TestRailClient):
    section_id = 4118  # testing_client section in the sandbox project
    case_data = {
        "title": "This is a test test case",
        "type_id": 1,
        "priority_id": 3,
        "estimate": "3m",
        "refs": "RF-1, RF-2",
        "custom_steps_separated": [
            {"content": "Step 1", "expected": "Expected Result 1"},
            {"content": "Step 2", "expected": "Expected Result 2"},
        ],
    }
    response = testrail_client.add_case(section_id=section_id, data=case_data)
    yield response
    testrail_client.delete_case(case_id=response["id"])
