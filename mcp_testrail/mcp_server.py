from typing import Dict

from fastmcp import FastMCP

from .testrail_client import TestRailClient


class TestRailMCPServer(FastMCP):
    def __init__(
        self,
        base_url: str = None,
        username: str = None,
        api_key: str = None,
    ):
        super().__init__(name="TestRail MCP Server")
        self._register_tools()
        with TestRailClient(base_url, username, api_key) as client:
            self.client = client

    def _register_tools(self):
        @self.tool()
        def get_projects():
            """Get projects"""
            try:
                return self.client.get_projects()
            except Exception as e:
                print(f"Error in get_projects tool: {e}")
                return {"error": str(e)}

        @self.tool()
        def get_project(id: int):
            """Get project by ID"""
            return self.client.get_project(id)

        @self.tool()
        def add_project(data: Dict):
            """Create a new project"""
            return self.client.add_project(data)
