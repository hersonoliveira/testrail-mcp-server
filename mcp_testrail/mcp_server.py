from typing import Dict, List, Optional

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
        self.client = TestRailClient(base_url, username, api_key)
        self._register_tools()

    def __del__(self):
        """Clean up client when server is destroyed"""
        if hasattr(self, "client"):
            self.client.close()

    def _handle_error(self, operation: str, error: Exception) -> Dict:
        """Standard error handling for all tools"""
        error_msg = f"Error in {operation}: {str(error)}"
        print(error_msg)
        return {"error": error_msg}

    def _register_tools(self):
        # ========== PROJECTS ==========

        @self.tool()
        def get_projects(
            is_completed: Optional[int] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ):
            """Get all projects with optional filtering"""
            try:
                return self.client.get_projects(
                    is_completed=is_completed, limit=limit, offset=offset
                )
            except Exception as e:
                return self._handle_error("get_projects", e)

        @self.tool()
        def get_project(project_id: int):
            """Get project by ID"""
            try:
                return self.client.get_project(project_id)
            except Exception as e:
                return self._handle_error("get_project", e)

        @self.tool()
        def add_project(data: Dict):
            """Create a new project"""
            try:
                return self.client.add_project(data)
            except Exception as e:
                return self._handle_error("add_project", e)

        @self.tool()
        def update_project(project_id: int, data: Dict):
            """Update an existing project"""
            try:
                return self.client.update_project(project_id, data)
            except Exception as e:
                return self._handle_error("update_project", e)

        @self.tool()
        def delete_project(project_id: int):
            """Delete a project"""
            try:
                return self.client.delete_project(project_id)
            except Exception as e:
                return self._handle_error("delete_project", e)

        @self.tool()
        def get_project_by_name(project_name: str):
            """Find a project by name"""
            try:
                return self.client.get_project_by_name(project_name)
            except Exception as e:
                return self._handle_error("get_project_by_name", e)

        # ========== SUITES ==========

        @self.tool()
        def get_suites(project_id: int):
            """Get all test suites for a project"""
            try:
                return self.client.get_suites(project_id)
            except Exception as e:
                return self._handle_error("get_suites", e)

        @self.tool()
        def get_suite(suite_id: int):
            """Get a test suite by ID"""
            try:
                return self.client.get_suite(suite_id)
            except Exception as e:
                return self._handle_error("get_suite", e)

        @self.tool()
        def add_suite(project_id: int, data: Dict):
            """Add a test suite to a project"""
            try:
                return self.client.add_suite(project_id, data)
            except Exception as e:
                return self._handle_error("add_suite", e)

        @self.tool()
        def update_suite(suite_id: int, data: Dict):
            """Update a test suite"""
            try:
                return self.client.update_suite(suite_id, data)
            except Exception as e:
                return self._handle_error("update_suite", e)

        @self.tool()
        def delete_suite(suite_id: int, soft: Optional[int] = None):
            """Delete a test suite"""
            try:
                return self.client.delete_suite(suite_id, soft=soft)
            except Exception as e:
                return self._handle_error("delete_suite", e)

        @self.tool()
        def get_suite_by_name(project_id: int, suite_name: str):
            """Find a suite by name in a project"""
            try:
                return self.client.get_suite_by_name(project_id, suite_name)
            except Exception as e:
                return self._handle_error("get_suite_by_name", e)

        # ========== CASES ==========

        @self.tool()
        def get_cases(
            project_id: int,
            suite_id: Optional[int] = None,
            section_id: Optional[int] = None,
            created_after: Optional[int] = None,
            created_before: Optional[int] = None,
            created_by: Optional[List[int]] = None,
            milestone_id: Optional[List[int]] = None,
            priority_id: Optional[List[int]] = None,
            type_id: Optional[List[int]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ):
            """Get test cases for a project with optional filters"""
            try:
                return self.client.get_cases(
                    project_id=project_id,
                    suite_id=suite_id,
                    section_id=section_id,
                    created_after=created_after,
                    created_before=created_before,
                    created_by=created_by,
                    milestone_id=milestone_id,
                    priority_id=priority_id,
                    type_id=type_id,
                    limit=limit,
                    offset=offset,
                )
            except Exception as e:
                return self._handle_error("get_cases", e)

        @self.tool()
        def get_case(case_id: int):
            """Get a test case by ID"""
            try:
                return self.client.get_case(case_id)
            except Exception as e:
                return self._handle_error("get_case", e)

        @self.tool()
        def add_case(section_id: int, data: Dict):
            """Add a new test case to a section"""
            try:
                return self.client.add_case(section_id, data)
            except Exception as e:
                return self._handle_error("add_case", e)

        @self.tool()
        def update_case(case_id: int, data: Dict):
            """Update an existing test case"""
            try:
                return self.client.update_case(case_id, data)
            except Exception as e:
                return self._handle_error("update_case", e)

        @self.tool()
        def update_cases(suite_id: int, data: Dict):
            """Update multiple test cases"""
            try:
                return self.client.update_cases(suite_id, data)
            except Exception as e:
                return self._handle_error("update_cases", e)

        @self.tool()
        def copy_cases_to_section(section_id: int, data: Dict):
            """Copy test cases to a section"""
            try:
                return self.client.copy_cases_to_section(section_id, data)
            except Exception as e:
                return self._handle_error("copy_cases_to_section", e)

        @self.tool()
        def move_cases_to_section(section_id: int, data: Dict):
            """Move test cases to a section"""
            try:
                return self.client.move_cases_to_section(section_id, data)
            except Exception as e:
                return self._handle_error("move_cases_to_section", e)

        @self.tool()
        def delete_case(case_id: int, soft: Optional[int] = None):
            """Delete a test case"""
            try:
                return self.client.delete_case(case_id, soft=soft)
            except Exception as e:
                return self._handle_error("delete_case", e)

        @self.tool()
        def delete_cases(suite_id: int, data: Dict, soft: Optional[int] = None):
            """Delete multiple test cases"""
            try:
                return self.client.delete_cases(suite_id, data, soft=soft)
            except Exception as e:
                return self._handle_error("delete_cases", e)

        @self.tool()
        def bulk_add_cases(section_id: int, cases_data: List[Dict]):
            """Helper to add multiple cases at once"""
            try:
                return self.client.bulk_add_cases(section_id, cases_data)
            except Exception as e:
                return self._handle_error("bulk_add_cases", e)

        # ========== MILESTONES ==========

        @self.tool()
        def get_milestones(
            project_id: int,
            is_completed: Optional[int] = None,
            is_started: Optional[int] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ):
            """Get milestones for a project"""
            try:
                return self.client.get_milestones(
                    project_id,
                    is_completed=is_completed,
                    is_started=is_started,
                    limit=limit,
                    offset=offset,
                )
            except Exception as e:
                return self._handle_error("get_milestones", e)

        @self.tool()
        def get_milestone(milestone_id: int):
            """Get a milestone by ID"""
            try:
                return self.client.get_milestone(milestone_id)
            except Exception as e:
                return self._handle_error("get_milestone", e)

        @self.tool()
        def add_milestone(project_id: int, data: Dict):
            """Add a milestone to a project"""
            try:
                return self.client.add_milestone(project_id, data)
            except Exception as e:
                return self._handle_error("add_milestone", e)

        @self.tool()
        def update_milestone(milestone_id: int, data: Dict):
            """Update a milestone"""
            try:
                return self.client.update_milestone(milestone_id, data)
            except Exception as e:
                return self._handle_error("update_milestone", e)

        @self.tool()
        def delete_milestone(milestone_id: int):
            """Delete a milestone"""
            try:
                return self.client.delete_milestone(milestone_id)
            except Exception as e:
                return self._handle_error("delete_milestone", e)

        @self.tool()
        def get_milestone_by_name(project_id: int, milestone_name: str):
            """Find a milestone by name in a project"""
            try:
                return self.client.get_milestone_by_name(project_id, milestone_name)
            except Exception as e:
                return self._handle_error("get_milestone_by_name", e)

        # ========== PLANS ==========

        @self.tool()
        def get_plans(
            project_id: int,
            created_after: Optional[int] = None,
            created_before: Optional[int] = None,
            created_by: Optional[List[int]] = None,
            is_completed: Optional[int] = None,
            limit: Optional[int] = None,
            milestone_id: Optional[List[int]] = None,
            offset: Optional[int] = None,
        ):
            """Get test plans for a project"""
            try:
                return self.client.get_plans(
                    project_id,
                    created_after=created_after,
                    created_before=created_before,
                    created_by=created_by,
                    is_completed=is_completed,
                    limit=limit,
                    milestone_id=milestone_id,
                    offset=offset,
                )
            except Exception as e:
                return self._handle_error("get_plans", e)

        @self.tool()
        def get_plan(plan_id: int):
            """Get a test plan by ID"""
            try:
                return self.client.get_plan(plan_id)
            except Exception as e:
                return self._handle_error("get_plan", e)

        @self.tool()
        def add_plan(project_id: int, data: Dict):
            """Add a test plan to a project"""
            try:
                return self.client.add_plan(project_id, data)
            except Exception as e:
                return self._handle_error("add_plan", e)

        @self.tool()
        def add_plan_entry(plan_id: int, data: Dict):
            """Add an entry to a test plan"""
            try:
                return self.client.add_plan_entry(plan_id, data)
            except Exception as e:
                return self._handle_error("add_plan_entry", e)

        @self.tool()
        def update_plan(plan_id: int, data: Dict):
            """Update a test plan"""
            try:
                return self.client.update_plan(plan_id, data)
            except Exception as e:
                return self._handle_error("update_plan", e)

        @self.tool()
        def update_plan_entry(plan_id: int, entry_id: int, data: Dict):
            """Update a test plan entry"""
            try:
                return self.client.update_plan_entry(plan_id, entry_id, data)
            except Exception as e:
                return self._handle_error("update_plan_entry", e)

        @self.tool()
        def close_plan(plan_id: int):
            """Close a test plan"""
            try:
                return self.client.close_plan(plan_id)
            except Exception as e:
                return self._handle_error("close_plan", e)

        @self.tool()
        def delete_plan(plan_id: int):
            """Delete a test plan"""
            try:
                return self.client.delete_plan(plan_id)
            except Exception as e:
                return self._handle_error("delete_plan", e)

        @self.tool()
        def delete_plan_entry(plan_id: int, entry_id: int):
            """Delete a test plan entry"""
            try:
                return self.client.delete_plan_entry(plan_id, entry_id)
            except Exception as e:
                return self._handle_error("delete_plan_entry", e)

        # ========== RUNS ==========

        @self.tool()
        def get_runs(
            project_id: int,
            created_after: Optional[int] = None,
            created_before: Optional[int] = None,
            created_by: Optional[List[int]] = None,
            is_completed: Optional[int] = None,
            limit: Optional[int] = None,
            milestone_id: Optional[List[int]] = None,
            offset: Optional[int] = None,
            suite_id: Optional[List[int]] = None,
        ):
            """Get test runs for a project"""
            try:
                return self.client.get_runs(
                    project_id,
                    created_after=created_after,
                    created_before=created_before,
                    created_by=created_by,
                    is_completed=is_completed,
                    limit=limit,
                    milestone_id=milestone_id,
                    offset=offset,
                    suite_id=suite_id,
                )
            except Exception as e:
                return self._handle_error("get_runs", e)

        @self.tool()
        def get_run(run_id: int):
            """Get a test run by ID"""
            try:
                return self.client.get_run(run_id)
            except Exception as e:
                return self._handle_error("get_run", e)

        @self.tool()
        def add_run(project_id: int, data: Dict):
            """Add a new test run to a project"""
            try:
                return self.client.add_run(project_id, data)
            except Exception as e:
                return self._handle_error("add_run", e)

        @self.tool()
        def update_run(run_id: int, data: Dict):
            """Update a test run"""
            try:
                return self.client.update_run(run_id, data)
            except Exception as e:
                return self._handle_error("update_run", e)

        @self.tool()
        def close_run(run_id: int):
            """Close a test run"""
            try:
                return self.client.close_run(run_id)
            except Exception as e:
                return self._handle_error("close_run", e)

        @self.tool()
        def delete_run(run_id: int):
            """Delete a test run"""
            try:
                return self.client.delete_run(run_id)
            except Exception as e:
                return self._handle_error("delete_run", e)

        @self.tool()
        def get_run_by_name(project_id: int, run_name: str):
            """Find a run by name in a project"""
            try:
                return self.client.get_run_by_name(project_id, run_name)
            except Exception as e:
                return self._handle_error("get_run_by_name", e)

        # ========== TESTS ==========

        @self.tool()
        def get_tests(
            run_id: int,
            status_id: Optional[List[int]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ):
            """Get tests for a test run"""
            try:
                return self.client.get_tests(
                    run_id, status_id=status_id, limit=limit, offset=offset
                )
            except Exception as e:
                return self._handle_error("get_tests", e)

        @self.tool()
        def get_test(test_id: int):
            """Get a test by ID"""
            try:
                return self.client.get_test(test_id)
            except Exception as e:
                return self._handle_error("get_test", e)

        # ========== RESULTS ==========

        @self.tool()
        def get_results(
            test_id: int,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            status_id: Optional[List[int]] = None,
        ):
            """Get results for a test"""
            try:
                return self.client.get_results(
                    test_id, limit=limit, offset=offset, status_id=status_id
                )
            except Exception as e:
                return self._handle_error("get_results", e)

        @self.tool()
        def get_results_for_case(
            run_id: int,
            case_id: int,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            status_id: Optional[List[int]] = None,
        ):
            """Get results for a test case in a specific run"""
            try:
                return self.client.get_results_for_case(
                    run_id, case_id, limit=limit, offset=offset, status_id=status_id
                )
            except Exception as e:
                return self._handle_error("get_results_for_case", e)

        @self.tool()
        def get_results_for_run(
            run_id: int,
            created_after: Optional[int] = None,
            created_before: Optional[int] = None,
            created_by: Optional[List[int]] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            status_id: Optional[List[int]] = None,
        ):
            """Get results for a test run"""
            try:
                return self.client.get_results_for_run(
                    run_id,
                    created_after=created_after,
                    created_before=created_before,
                    created_by=created_by,
                    limit=limit,
                    offset=offset,
                    status_id=status_id,
                )
            except Exception as e:
                return self._handle_error("get_results_for_run", e)

        @self.tool()
        def add_result(test_id: int, data: Dict):
            """Add a result for a test"""
            try:
                return self.client.add_result(test_id, data)
            except Exception as e:
                return self._handle_error("add_result", e)

        @self.tool()
        def add_result_for_case(run_id: int, case_id: int, data: Dict):
            """Add a result for a test case in a test run"""
            try:
                return self.client.add_result_for_case(run_id, case_id, data)
            except Exception as e:
                return self._handle_error("add_result_for_case", e)

        @self.tool()
        def add_results(run_id: int, data: Dict):
            """Add multiple results for a test run"""
            try:
                return self.client.add_results(run_id, data)
            except Exception as e:
                return self._handle_error("add_results", e)

        @self.tool()
        def add_results_for_cases(run_id: int, data: Dict):
            """Add results for multiple test cases"""
            try:
                return self.client.add_results_for_cases(run_id, data)
            except Exception as e:
                return self._handle_error("add_results_for_cases", e)

        # ========== USERS ==========

        @self.tool()
        def get_users(limit: Optional[int] = None, offset: Optional[int] = None):
            """Get all users"""
            try:
                return self.client.get_users(limit=limit, offset=offset)
            except Exception as e:
                return self._handle_error("get_users", e)

        @self.tool()
        def get_user(user_id: int):
            """Get a user by ID"""
            try:
                return self.client.get_user(user_id)
            except Exception as e:
                return self._handle_error("get_user", e)

        @self.tool()
        def get_user_by_email(email: str):
            """Get a user by email"""
            try:
                return self.client.get_user_by_email(email)
            except Exception as e:
                return self._handle_error("get_user_by_email", e)

        @self.tool()
        def get_current_user():
            """Get current user"""
            try:
                return self.client.get_current_user()
            except Exception as e:
                return self._handle_error("get_current_user", e)

        @self.tool()
        def get_user_by_name(username: str):
            """Find a user by name"""
            try:
                return self.client.get_user_by_name(username)
            except Exception as e:
                return self._handle_error("get_user_by_name", e)

        # ========== UTILITY TOOLS ==========

        @self.tool()
        def get_case_fields():
            """Get available case fields"""
            try:
                return self.client.get_case_fields()
            except Exception as e:
                return self._handle_error("get_case_fields", e)

        @self.tool()
        def get_case_types():
            """Get available case types"""
            try:
                return self.client.get_case_types()
            except Exception as e:
                return self._handle_error("get_case_types", e)

        @self.tool()
        def get_priorities():
            """Get available priorities"""
            try:
                return self.client.get_priorities()
            except Exception as e:
                return self._handle_error("get_priorities", e)

        @self.tool()
        def get_statuses():
            """Get available statuses"""
            try:
                return self.client.get_statuses()
            except Exception as e:
                return self._handle_error("get_statuses", e)

        @self.tool()
        def get_result_fields():
            """Get available result fields"""
            try:
                return self.client.get_result_fields()
            except Exception as e:
                return self._handle_error("get_result_fields", e)

        @self.tool()
        def get_templates(project_id: int):
            """Get available templates for a project"""
            try:
                return self.client.get_templates(project_id)
            except Exception as e:
                return self._handle_error("get_templates", e)

        # ========== SECTIONS ==========

        @self.tool()
        def get_section_by_name(project_id: int, section_name: str):
            """Find a section by name in a project"""
            try:
                return self.client.get_section_by_name(project_id, section_name)
            except Exception as e:
                return self._handle_error("get_section_by_name", e)

        @self.tool()
        def get_sections(
            project_id: int,
            suite_id: Optional[int] = None,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ):
            """Get sections for a project"""
            try:
                return self.client.get_sections(
                    project_id, suite_id=suite_id, limit=limit, offset=offset
                )
            except Exception as e:
                return self._handle_error("get_sections", e)

        @self.tool()
        def get_section(section_id: int):
            """Get a section by ID"""
            try:
                return self.client.get_section(section_id)
            except Exception as e:
                return self._handle_error("get_section", e)

        @self.tool()
        def add_section(project_id: int, data: Dict):
            """Add a section to a project"""
            try:
                return self.client.add_section(project_id, data)
            except Exception as e:
                return self._handle_error("add_section", e)

        @self.tool()
        def update_section(section_id: int, data: Dict):
            """Update a section"""
            try:
                return self.client.update_section(section_id, data)
            except Exception as e:
                return self._handle_error("update_section", e)

        @self.tool()
        def move_section(section_id: int, data: Dict):
            """Move a section"""
            try:
                return self.client.move_section(section_id, data)
            except Exception as e:
                return self._handle_error("move_section", e)

        @self.tool()
        def delete_section(section_id: int, soft: Optional[int] = None):
            """Delete a section"""
            try:
                return self.client.delete_section(section_id, soft=soft)
            except Exception as e:
                return self._handle_error("delete_section", e)

        # ========== ATTACHMENT TOOLS ==========

        @self.tool()
        def add_attachment_to_case(case_id: int, file_path: str):
            """Add an attachment to a test case"""
            try:
                return self.client.add_attachment_to_case(case_id, file_path)
            except Exception as e:
                return self._handle_error("add_attachment_to_case", e)

        @self.tool()
        def add_attachment_to_result(result_id: int, file_path: str):
            """Add an attachment to a test result"""
            try:
                return self.client.add_attachment_to_result(result_id, file_path)
            except Exception as e:
                return self._handle_error("add_attachment_to_result", e)

        @self.tool()
        def add_attachment_to_run(run_id: int, file_path: str):
            """Add an attachment to a test run"""
            try:
                return self.client.add_attachment_to_run(run_id, file_path)
            except Exception as e:
                return self._handle_error("add_attachment_to_run", e)

        @self.tool()
        def add_attachment_to_plan(plan_id: int, file_path: str):
            """Add an attachment to a test plan"""
            try:
                return self.client.add_attachment_to_plan(plan_id, file_path)
            except Exception as e:
                return self._handle_error("add_attachment_to_plan", e)

        @self.tool()
        def delete_attachment(attachment_id: int):
            """Delete an attachment"""
            try:
                return self.client.delete_attachment(attachment_id)
            except Exception as e:
                return self._handle_error("delete_attachment", e)


def create_server(base_url: str, username: str, api_key: str) -> TestRailMCPServer:
    """Factory function to create a TestRail MCP Server instance"""
    return TestRailMCPServer(base_url=base_url, username=username, api_key=api_key)
