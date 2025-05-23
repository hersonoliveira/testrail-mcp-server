# from unittest.mock import MagicMock, patch

# import httpx
# import pytest

# from mcp_testrail.testrail_client import TestRailClient


# # Define a fixture for the TestRailClient
# @pytest.fixture
# def testrail_client():
#     """Fixture for TestRailClient instance."""
#     return TestRailClient(
#         base_url="https://fake.testrail.io", username="test_user", api_key="fake_key"
#     )


# # Test get_projects method
# @patch("mcp_testrail.testrail_client.TestRailClient._send_request")
# def test_get_projects(mock_send_request, testrail_client):
#     """Test get_projects calls _send_request with correct parameters."""
#     mock_send_request.return_value = [{"id": 1, "name": "Project 1"}]
#     projects = testrail_client.get_projects()

#     mock_send_request.assert_called_once_with("GET", "get_projects")
#     assert isinstance(projects, list)
#     assert len(projects) > 0
#     assert projects[0]["name"] == "Project 1"


# # Test get_project method
# @patch("mcp_testrail.testrail_client.TestRailClient._send_request")
# def test_get_project(mock_send_request, testrail_client):
#     """Test get_project calls _send_request with correct parameters."""
#     project_id = 123
#     mock_send_request.return_value = {"id": project_id, "name": "Specific Project"}
#     project = testrail_client.get_project(project_id)

#     mock_send_request.assert_called_once_with("GET", f"get_project/{project_id}")
#     assert isinstance(project, dict)
#     assert project["id"] == project_id
#     assert project["name"] == "Specific Project"


# # Test error handling in _send_request
# @patch("mcp_testrail.testrail_client.httpx.Client")
# def test_send_request_error_handling(mock_httpx_client, testrail_client):
#     """Test _send_request raises exception on non-2xx status code."""
#     mock_response = MagicMock()
#     mock_response.status_code = 400
#     mock_response.json.side_effect = httpx.HTTPStatusError(
#         "Bad Request", request=MagicMock(), response=mock_response
#     )
#     mock_response.text = "Error details from API"

#     mock_client_instance = MagicMock()
#     mock_httpx_client.return_value.__enter__.return_value = mock_client_instance
#     mock_client_instance.request.return_value = mock_response

#     with pytest.raises(Exception) as excinfo:
#         testrail_client._send_request("GET", "some_endpoint")

#     assert "TestRail API returned HTTP 400" in str(excinfo.value)
#     assert "Error details from API" in str(excinfo.value)
