"""
Integration tests for TestRailClient using real API calls.

These tests require actual TestRail API credentials and will make real HTTP requests.
Set the following environment variables before running:
- TESTRAIL_URL
- TESTRAIL_USERNAME
- TESTRAIL_API_KEY
- TESTRAIL_PROJECT_ID (optional, defaults to 1)

Run with: pytest -m integration
"""

import pytest
from dotenv import load_dotenv

from mcp_testrail.testrail_client import TestRailClient as trclient

load_dotenv()


@pytest.mark.integration
class TestProjectIntegration:
    """Integration tests for project methods"""

    def test_get_projects(self, testrail_client: trclient):
        response = testrail_client.get_projects()

        assert isinstance(response["projects"], list)
        if response:
            project = response["projects"][0]
            assert "id" in project
            assert "name" in project
            assert isinstance(project["id"], int)
            assert isinstance(project["name"], str)

    def test_get_project_by_name(
        self, testrail_client: trclient, test_project_name: str
    ):
        response = testrail_client.get_project_by_name(test_project_name)

        if response:
            assert "id" in response
            assert test_project_name == response["name"]


@pytest.mark.integration
class TestCasesIntegration:
    """Integration tests for cases methods"""

    def test_get_cases_from_section(self, testrail_client: trclient):
        project_id = 5  # sandbox
        section_id = 206
        response = testrail_client.get_cases(
            project_id=project_id, section_id=section_id, limit=2
        )
        assert isinstance(response["cases"], list)
        assert response["size"] == 2

    def test_add_case(self, new_test_case):
        assert new_test_case["title"] == "This is a test test case"
