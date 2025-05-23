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

from mcp_testrail.testrail_client import TestRailClient as trclient


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
