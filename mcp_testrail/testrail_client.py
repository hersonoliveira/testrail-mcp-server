import base64
from typing import Dict, List, Optional, Union

import httpx


class TestRailClient:
    """
    A comprehensive client for interacting with the TestRail API using httpx.

    TestRail API uses Basic Authentication and accepts/returns JSON data.
    """

    def __init__(self, base_url: str, username: str, api_key: str):
        """
        Initialize the TestRail API client.

        Args:
            base_url: The base URL of your TestRail instance (e.g., 'https://example.testrail.io/')
            username: TestRail username or email address
            api_key: TestRail password or API key
        """

        if not base_url.endswith("/"):
            base_url += "/"

        self.base_url = f"{base_url}index.php?/api/v2/"
        self.auth = str(
            base64.b64encode(bytes("%s:%s" % (username, api_key), "utf-8")), "ascii"
        ).strip()
        self.session = httpx.Client()
        self.session.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth}",
        }

    def _send_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Union[Dict, List]:
        """
        Send a request to the TestRail API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint to call
            data: Request data for POST requests
            files: Files for upload
            params: URL parameters

        Returns:
            Response data as a dictionary or list
        """
        url = f"{self.base_url}{endpoint}"

        kwargs = {"method": method, "url": url}

        if params:
            kwargs["params"] = params

        if files:
            # For file uploads, don't set JSON content type
            headers = {
                k: v for k, v in self.session.headers.items() if k != "Content-Type"
            }
            kwargs["headers"] = headers
            kwargs["files"] = files
            if data:
                kwargs["data"] = data
        elif data:
            kwargs["json"] = data

        response = self.session.request(**kwargs)

        # Check for errors
        if response.status_code >= 400:
            error_msg = f"TestRail API returned HTTP {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    error_msg += f": {error_data['error']}"
            except Exception:
                error_msg += f": {response.text}"

            raise Exception(error_msg)

        # Return JSON response if available, otherwise return text
        try:
            return response.json()
        except Exception:
            return {"text": response.text}

    def close(self):
        """Close the HTTP session"""
        self.session.close()

    # ========== CASES ==========

    def get_case(self, case_id: int) -> Dict:
        """Get a test case by ID"""
        return self._send_request("GET", f"get_case/{case_id}")

    def get_cases(
        self,
        project_id: int,
        suite_id: Optional[int] = None,
        section_id: Optional[int] = None,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[List[int]] = None,
        milestone_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        template_id: Optional[List[int]] = None,
        type_id: Optional[List[int]] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get test cases for a project with optional filters"""
        params = {}
        if suite_id:
            params["suite_id"] = suite_id
        if section_id:
            params["section_id"] = section_id
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if created_by:
            params["created_by"] = ",".join(map(str, created_by))
        if milestone_id:
            params["milestone_id"] = ",".join(map(str, milestone_id))
        if priority_id:
            params["priority_id"] = ",".join(map(str, priority_id))
        if template_id:
            params["template_id"] = ",".join(map(str, template_id))
        if type_id:
            params["type_id"] = ",".join(map(str, type_id))
        if updated_after:
            params["updated_after"] = updated_after
        if updated_before:
            params["updated_before"] = updated_before
        if updated_by:
            params["updated_by"] = ",".join(map(str, updated_by))
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_cases/{project_id}", params=params)

    def add_case(self, section_id: int, data: Dict) -> Dict:
        """Add a new test case to a section"""
        return self._send_request("POST", f"add_case/{section_id}", data=data)

    def copy_cases_to_section(self, section_id: int, data: Dict) -> Dict:
        """Copy test cases to a section"""
        return self._send_request(
            "POST", f"copy_cases_to_section/{section_id}", data=data
        )

    def update_case(self, case_id: int, data: Dict) -> Dict:
        """Update an existing test case"""
        return self._send_request("POST", f"update_case/{case_id}", data=data)

    def update_cases(self, suite_id: int, data: Dict) -> List[Dict]:
        """Update multiple test cases"""
        return self._send_request("POST", f"update_cases/{suite_id}", data=data)

    def move_cases_to_section(self, section_id: int, data: Dict) -> Dict:
        """Move test cases to a section"""
        return self._send_request(
            "POST", f"move_cases_to_section/{section_id}", data=data
        )

    def delete_case(self, case_id: int, soft: Optional[int] = None) -> Dict:
        """Delete a test case"""
        params = {}
        if soft is not None:
            params["soft"] = soft
        return self._send_request("POST", f"delete_case/{case_id}", params=params)

    def delete_cases(
        self, suite_id: int, data: Dict, soft: Optional[int] = None
    ) -> Dict:
        """Delete multiple test cases"""
        params = {}
        if soft is not None:
            params["soft"] = soft
        return self._send_request(
            "POST", f"delete_cases/{suite_id}", data=data, params=params
        )

    # ========== CASE FIELDS ==========

    def get_case_fields(self) -> List[Dict]:
        """Get available case fields"""
        return self._send_request("GET", "get_case_fields")

    def add_case_field(self, data: Dict) -> Dict:
        """Add a new case field"""
        return self._send_request("POST", "add_case_field", data=data)

    # ========== CASE TYPES ==========

    def get_case_types(self) -> List[Dict]:
        """Get available case types"""
        return self._send_request("GET", "get_case_types")

    # ========== CONFIGURATIONS ==========

    def get_configs(self, project_id: int) -> List[Dict]:
        """Get configurations for a project"""
        return self._send_request("GET", f"get_configs/{project_id}")

    def add_config_group(self, project_id: int, data: Dict) -> Dict:
        """Add a configuration group"""
        return self._send_request("POST", f"add_config_group/{project_id}", data=data)

    def add_config(self, config_group_id: int, data: Dict) -> Dict:
        """Add a configuration"""
        return self._send_request("POST", f"add_config/{config_group_id}", data=data)

    def update_config_group(self, config_group_id: int, data: Dict) -> Dict:
        """Update a configuration group"""
        return self._send_request(
            "POST", f"update_config_group/{config_group_id}", data=data
        )

    def update_config(self, config_id: int, data: Dict) -> Dict:
        """Update a configuration"""
        return self._send_request("POST", f"update_config/{config_id}", data=data)

    def delete_config_group(self, config_group_id: int) -> Dict:
        """Delete a configuration group"""
        return self._send_request("POST", f"delete_config_group/{config_group_id}")

    def delete_config(self, config_id: int) -> Dict:
        """Delete a configuration"""
        return self._send_request("POST", f"delete_config/{config_id}")

    # ========== MILESTONES ==========

    def get_milestone(self, milestone_id: int) -> Dict:
        """Get a milestone by ID"""
        return self._send_request("GET", f"get_milestone/{milestone_id}")

    def get_milestones(
        self,
        project_id: int,
        is_completed: Optional[int] = None,
        is_started: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get milestones for a project"""
        params = {}
        if is_completed is not None:
            params["is_completed"] = is_completed
        if is_started is not None:
            params["is_started"] = is_started
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_milestones/{project_id}", params=params)

    def add_milestone(self, project_id: int, data: Dict) -> Dict:
        """Add a milestone to a project"""
        return self._send_request("POST", f"add_milestone/{project_id}", data=data)

    def update_milestone(self, milestone_id: int, data: Dict) -> Dict:
        """Update a milestone"""
        return self._send_request("POST", f"update_milestone/{milestone_id}", data=data)

    def delete_milestone(self, milestone_id: int) -> Dict:
        """Delete a milestone"""
        return self._send_request("POST", f"delete_milestone/{milestone_id}")

    # ========== PLANS ==========

    def get_plan(self, plan_id: int) -> Dict:
        """Get a test plan by ID"""
        return self._send_request("GET", f"get_plan/{plan_id}")

    def get_plans(
        self,
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[List[int]] = None,
        is_completed: Optional[int] = None,
        limit: Optional[int] = None,
        milestone_id: Optional[List[int]] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get test plans for a project"""
        params = {}
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if created_by:
            params["created_by"] = ",".join(map(str, created_by))
        if is_completed is not None:
            params["is_completed"] = is_completed
        if limit:
            params["limit"] = limit
        if milestone_id:
            params["milestone_id"] = ",".join(map(str, milestone_id))
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_plans/{project_id}", params=params)

    def add_plan(self, project_id: int, data: Dict) -> Dict:
        """Add a test plan to a project"""
        return self._send_request("POST", f"add_plan/{project_id}", data=data)

    def add_plan_entry(self, plan_id: int, data: Dict) -> Dict:
        """Add an entry to a test plan"""
        return self._send_request("POST", f"add_plan_entry/{plan_id}", data=data)

    def update_plan(self, plan_id: int, data: Dict) -> Dict:
        """Update a test plan"""
        return self._send_request("POST", f"update_plan/{plan_id}", data=data)

    def update_plan_entry(self, plan_id: int, entry_id: int, data: Dict) -> Dict:
        """Update a test plan entry"""
        return self._send_request(
            "POST", f"update_plan_entry/{plan_id}/{entry_id}", data=data
        )

    def close_plan(self, plan_id: int) -> Dict:
        """Close a test plan"""
        return self._send_request("POST", f"close_plan/{plan_id}")

    def delete_plan(self, plan_id: int) -> Dict:
        """Delete a test plan"""
        return self._send_request("POST", f"delete_plan/{plan_id}")

    def delete_plan_entry(self, plan_id: int, entry_id: int) -> Dict:
        """Delete a test plan entry"""
        return self._send_request("POST", f"delete_plan_entry/{plan_id}/{entry_id}")

    # ========== PRIORITIES ==========

    def get_priorities(self) -> List[Dict]:
        """Get available priorities"""
        return self._send_request("GET", "get_priorities")

    # ========== PROJECTS ==========

    def get_project(self, project_id: int) -> Dict:
        """Get a project by ID"""
        return self._send_request("GET", f"get_project/{project_id}")

    def get_projects(
        self,
        is_completed: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get all projects"""
        params = {}
        if is_completed is not None:
            params["is_completed"] = is_completed
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", "get_projects", params=params)

    def add_project(self, data: Dict) -> Dict:
        """Add a new project"""
        return self._send_request("POST", "add_project", data=data)

    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update a project"""
        return self._send_request("POST", f"update_project/{project_id}", data=data)

    def delete_project(self, project_id: int) -> Dict:
        """Delete a project"""
        return self._send_request("POST", f"delete_project/{project_id}")

    # ========== REPORTS ==========

    def get_reports(self, project_id: int) -> List[Dict]:
        """Get available reports for a project"""
        return self._send_request("GET", f"get_reports/{project_id}")

    def run_report(self, report_template_id: int) -> Dict:
        """Run a report"""
        return self._send_request("GET", f"run_report/{report_template_id}")

    # ========== RESULTS ==========

    def get_results(
        self,
        test_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status_id: Optional[List[int]] = None,
    ) -> List[Dict]:
        """Get results for a test"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if status_id:
            params["status_id"] = ",".join(map(str, status_id))

        return self._send_request("GET", f"get_results/{test_id}", params=params)

    def get_results_for_case(
        self,
        run_id: int,
        case_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status_id: Optional[List[int]] = None,
    ) -> List[Dict]:
        """Get results for a test case in a specific run"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if status_id:
            params["status_id"] = ",".join(map(str, status_id))

        return self._send_request(
            "GET", f"get_results_for_case/{run_id}/{case_id}", params=params
        )

    def get_results_for_run(
        self,
        run_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status_id: Optional[List[int]] = None,
    ) -> List[Dict]:
        """Get results for a test run"""
        params = {}
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if created_by:
            params["created_by"] = ",".join(map(str, created_by))
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if status_id:
            params["status_id"] = ",".join(map(str, status_id))

        return self._send_request("GET", f"get_results_for_run/{run_id}", params=params)

    def add_result(self, test_id: int, data: Dict) -> Dict:
        """Add a result for a test"""
        return self._send_request("POST", f"add_result/{test_id}", data=data)

    def add_result_for_case(self, run_id: int, case_id: int, data: Dict) -> Dict:
        """Add a result for a test case in a test run"""
        return self._send_request(
            "POST", f"add_result_for_case/{run_id}/{case_id}", data=data
        )

    def add_results(self, run_id: int, data: Dict) -> List[Dict]:
        """Add multiple results for a test run"""
        return self._send_request("POST", f"add_results/{run_id}", data=data)

    def add_results_for_cases(self, run_id: int, data: Dict) -> List[Dict]:
        """Add results for multiple test cases"""
        return self._send_request("POST", f"add_results_for_cases/{run_id}", data=data)

    # ========== RESULT FIELDS ==========

    def get_result_fields(self) -> List[Dict]:
        """Get available result fields"""
        return self._send_request("GET", "get_result_fields")

    # ========== RUNS ==========

    def get_run(self, run_id: int) -> Dict:
        """Get a test run by ID"""
        return self._send_request("GET", f"get_run/{run_id}")

    def get_runs(
        self,
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[List[int]] = None,
        is_completed: Optional[int] = None,
        limit: Optional[int] = None,
        milestone_id: Optional[List[int]] = None,
        offset: Optional[int] = None,
        suite_id: Optional[List[int]] = None,
    ) -> List[Dict]:
        """Get test runs for a project"""
        params = {}
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if created_by:
            params["created_by"] = ",".join(map(str, created_by))
        if is_completed is not None:
            params["is_completed"] = is_completed
        if limit:
            params["limit"] = limit
        if milestone_id:
            params["milestone_id"] = ",".join(map(str, milestone_id))
        if offset:
            params["offset"] = offset
        if suite_id:
            params["suite_id"] = ",".join(map(str, suite_id))

        return self._send_request("GET", f"get_runs/{project_id}", params=params)

    def add_run(self, project_id: int, data: Dict) -> Dict:
        """Add a new test run to a project"""
        return self._send_request("POST", f"add_run/{project_id}", data=data)

    def update_run(self, run_id: int, data: Dict) -> Dict:
        """Update a test run"""
        return self._send_request("POST", f"update_run/{run_id}", data=data)

    def close_run(self, run_id: int) -> Dict:
        """Close a test run"""
        return self._send_request("POST", f"close_run/{run_id}")

    def delete_run(self, run_id: int) -> Dict:
        """Delete a test run"""
        return self._send_request("POST", f"delete_run/{run_id}")

    # ========== SECTIONS ==========

    def get_section(self, section_id: int) -> Dict:
        """Get a section by ID"""
        return self._send_request("GET", f"get_section/{section_id}")

    def get_sections(
        self,
        project_id: int,
        suite_id: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get sections for a project"""
        params = {}
        if suite_id:
            params["suite_id"] = suite_id
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_sections/{project_id}", params=params)

    def add_section(self, project_id: int, data: Dict) -> Dict:
        """Add a section to a project"""
        return self._send_request("POST", f"add_section/{project_id}", data=data)

    def move_section(self, section_id: int, data: Dict) -> Dict:
        """Move a section"""
        return self._send_request("POST", f"move_section/{section_id}", data=data)

    def update_section(self, section_id: int, data: Dict) -> Dict:
        """Update a section"""
        return self._send_request("POST", f"update_section/{section_id}", data=data)

    def delete_section(self, section_id: int, soft: Optional[int] = None) -> Dict:
        """Delete a section"""
        params = {}
        if soft is not None:
            params["soft"] = soft
        return self._send_request("POST", f"delete_section/{section_id}", params=params)

    # ========== STATUSES ==========

    def get_statuses(self) -> List[Dict]:
        """Get available statuses"""
        return self._send_request("GET", "get_statuses")

    # ========== SUITES ==========

    def get_suite(self, suite_id: int) -> Dict:
        """Get a test suite by ID"""
        return self._send_request("GET", f"get_suite/{suite_id}")

    def get_suites(self, project_id: int) -> List[Dict]:
        """Get all test suites for a project"""
        return self._send_request("GET", f"get_suites/{project_id}")

    def add_suite(self, project_id: int, data: Dict) -> Dict:
        """Add a test suite to a project"""
        return self._send_request("POST", f"add_suite/{project_id}", data=data)

    def update_suite(self, suite_id: int, data: Dict) -> Dict:
        """Update a test suite"""
        return self._send_request("POST", f"update_suite/{suite_id}", data=data)

    def delete_suite(self, suite_id: int, soft: Optional[int] = None) -> Dict:
        """Delete a test suite"""
        params = {}
        if soft is not None:
            params["soft"] = soft
        return self._send_request("POST", f"delete_suite/{suite_id}", params=params)

    # ========== TEMPLATES ==========

    def get_templates(self, project_id: int) -> List[Dict]:
        """Get available templates for a project"""
        return self._send_request("GET", f"get_templates/{project_id}")

    # ========== TESTS ==========

    def get_test(self, test_id: int) -> Dict:
        """Get a test by ID"""
        return self._send_request("GET", f"get_test/{test_id}")

    def get_tests(
        self,
        run_id: int,
        status_id: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict]:
        """Get tests for a test run"""
        params = {}
        if status_id:
            params["status_id"] = ",".join(map(str, status_id))
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_tests/{run_id}", params=params)

    # ========== USERS ==========

    def get_user(self, user_id: int) -> Dict:
        """Get a user by ID"""
        return self._send_request("GET", f"get_user/{user_id}")

    def get_user_by_email(self, email: str) -> Dict:
        """Get a user by email"""
        return self._send_request("GET", "get_user_by_email", params={"email": email})

    def get_users(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Dict]:
        """Get all users"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", "get_users", params=params)

    def get_current_user(self) -> Dict:
        """Get current user"""
        return self._send_request("GET", "get_current_user")

    # ========== ATTACHMENTS ==========

    def add_attachment_to_case(self, case_id: int, file_path: str) -> Dict:
        """Add an attachment to a test case"""
        with open(file_path, "rb") as f:
            files = {"attachment": (file_path.split("/")[-1], f.read())}
        return self._send_request(
            "POST", f"add_attachment_to_case/{case_id}", files=files
        )

    def add_attachment_to_plan(self, plan_id: int, file_path: str) -> Dict:
        """Add an attachment to a test plan"""
        with open(file_path, "rb") as f:
            files = {"attachment": (file_path.split("/")[-1], f.read())}
        return self._send_request(
            "POST", f"add_attachment_to_plan/{plan_id}", files=files
        )

    def add_attachment_to_plan_entry(
        self, plan_id: int, entry_id: int, file_path: str
    ) -> Dict:
        """Add an attachment to a test plan entry"""
        with open(file_path, "rb") as f:
            files = {"attachment": (file_path.split("/")[-1], f.read())}
        return self._send_request(
            "POST", f"add_attachment_to_plan_entry/{plan_id}/{entry_id}", files=files
        )

    def add_attachment_to_result(self, result_id: int, file_path: str) -> Dict:
        """Add an attachment to a test result"""
        with open(file_path, "rb") as f:
            files = {"attachment": (file_path.split("/")[-1], f.read())}
        return self._send_request(
            "POST", f"add_attachment_to_result/{result_id}", files=files
        )

    def add_attachment_to_run(self, run_id: int, file_path: str) -> Dict:
        """Add an attachment to a test run"""
        with open(file_path, "rb") as f:
            files = {"attachment": (file_path.split("/")[-1], f.read())}
        return self._send_request(
            "POST", f"add_attachment_to_run/{run_id}", files=files
        )

    def get_attachment(self, attachment_id: int) -> bytes:
        """Get an attachment by ID"""
        response = self.session.get(f"{self.base_url}get_attachment/{attachment_id}")
        if response.status_code >= 400:
            raise Exception(f"Failed to get attachment: HTTP {response.status_code}")
        return response.content

    def delete_attachment(self, attachment_id: int) -> Dict:
        """Delete an attachment"""
        return self._send_request("POST", f"delete_attachment/{attachment_id}")

    # ========== SHARED STEPS ==========

    def get_shared_step(self, shared_step_id: int) -> Dict:
        """Get a shared step by ID"""
        return self._send_request("GET", f"get_shared_step/{shared_step_id}")

    def get_shared_steps(
        self,
        project_id: int,
        created_after: Optional[int] = None,
        created_before: Optional[int] = None,
        created_by: Optional[List[int]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        updated_after: Optional[int] = None,
        updated_before: Optional[int] = None,
        updated_by: Optional[List[int]] = None,
    ) -> List[Dict]:
        """Get shared steps for a project"""
        params = {}
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if created_by:
            params["created_by"] = ",".join(map(str, created_by))
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if updated_after:
            params["updated_after"] = updated_after
        if updated_before:
            params["updated_before"] = updated_before
        if updated_by:
            params["updated_by"] = ",".join(map(str, updated_by))

        return self._send_request(
            "GET", f"get_shared_steps/{project_id}", params=params
        )

    def add_shared_step(self, project_id: int, data: Dict) -> Dict:
        """Add a shared step to a project"""
        return self._send_request("POST", f"add_shared_step/{project_id}", data=data)

    def update_shared_step(self, shared_step_id: int, data: Dict) -> Dict:
        """Update a shared step"""
        return self._send_request(
            "POST", f"update_shared_step/{shared_step_id}", data=data
        )

    def delete_shared_step(
        self, shared_step_id: int, soft: Optional[int] = None
    ) -> Dict:
        """Delete a shared step"""
        params = {}
        if soft is not None:
            params["soft"] = soft
        return self._send_request(
            "POST", f"delete_shared_step/{shared_step_id}", params=params
        )

    # ========== VARIABLES ==========

    def get_variables(self, project_id: int) -> List[Dict]:
        """Get variables for a project"""
        return self._send_request("GET", f"get_variables/{project_id}")

    def add_variable(self, project_id: int, data: Dict) -> Dict:
        """Add a variable to a project"""
        return self._send_request("POST", f"add_variable/{project_id}", data=data)

    def update_variable(self, variable_id: int, data: Dict) -> Dict:
        """Update a variable"""
        return self._send_request("POST", f"update_variable/{variable_id}", data=data)

    def delete_variable(self, variable_id: int) -> Dict:
        """Delete a variable"""
        return self._send_request("POST", f"delete_variable/{variable_id}")

    # ========== BDD ==========

    def get_bdd_steps(
        self, project_id: int, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Dict]:
        """Get BDD steps for a project"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_bdd_steps/{project_id}", params=params)

    # ========== DATASETS ==========

    def get_datasets(
        self, project_id: int, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List[Dict]:
        """Get datasets for a project"""
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

        return self._send_request("GET", f"get_datasets/{project_id}", params=params)

    def add_dataset(self, project_id: int, data: Dict) -> Dict:
        """Add a dataset to a project"""
        return self._send_request("POST", f"add_dataset/{project_id}", data=data)

    def update_dataset(self, dataset_id: int, data: Dict) -> Dict:
        """Update a dataset"""
        return self._send_request("POST", f"update_dataset/{dataset_id}", data=data)

    def delete_dataset(self, dataset_id: int) -> Dict:
        """Delete a dataset"""
        return self._send_request("POST", f"delete_dataset/{dataset_id}")

    # ========== GROUPS ==========

    def get_groups(self) -> List[Dict]:
        """Get all groups"""
        return self._send_request("GET", "get_groups")

    def get_group(self, group_id: int) -> Dict:
        """Get a group by ID"""
        return self._send_request("GET", f"get_group/{group_id}")

    # ========== ROLES ==========

    def get_roles(self) -> List[Dict]:
        """Get all roles"""
        return self._send_request("GET", "get_roles")

    def get_role(self, role_id: int) -> Dict:
        """Get a role by ID"""
        return self._send_request("GET", f"get_role/{role_id}")

    # ========== HELPER METHODS ==========

    def bulk_add_cases(self, section_id: int, cases_data: List[Dict]) -> List[Dict]:
        """Helper method to add multiple cases at once"""
        results = []
        for case_data in cases_data:
            result = self.add_case(section_id, case_data)
            results.append(result)
        return results

    def get_project_by_name(self, project_name: str) -> Optional[Dict]:
        """Helper method to find a project by name"""
        result = self.get_projects()
        for project in result["projects"]:
            if project.get("name") == project_name:
                return project
        return None

    def get_suite_by_name(self, project_id: int, suite_name: str) -> Optional[Dict]:
        """Helper method to find a suite by name"""
        suites = self.get_suites(project_id)
        for suite in suites:
            if suite.get("name") == suite_name:
                return suite
        return None

    def get_run_by_name(self, project_id: int, run_name: str) -> Optional[Dict]:
        """Helper method to find a run by name"""
        runs = self.get_runs(project_id)
        for run in runs:
            if run.get("name") == run_name:
                return run
        return None

    def get_milestone_by_name(
        self, project_id: int, milestone_name: str
    ) -> Optional[Dict]:
        """Helper method to find a milestone by name"""
        milestones = self.get_milestones(project_id)
        for milestone in milestones:
            if milestone.get("name") == milestone_name:
                return milestone
        return None

    def get_user_by_name(self, username: str) -> Optional[Dict]:
        """Helper method to find a user by name"""
        users = self.get_users()
        for user in users:
            if user.get("name") == username:
                return user
        return None

    def wait_for_report(
        self,
        report_template_id: int,
        max_wait_seconds: int = 300,
        poll_interval: int = 5,
    ) -> Dict:
        """Helper method to wait for a report to complete"""
        import time

        start_time = time.time()
        while time.time() - start_time < max_wait_seconds:
            try:
                result = self.run_report(report_template_id)
                if result.get("status") == "completed":
                    return result
                elif result.get("status") == "error":
                    raise Exception(
                        f"Report failed: {result.get('error', 'Unknown error')}"
                    )

                time.sleep(poll_interval)
            except Exception as e:
                if "still being generated" in str(e).lower():
                    time.sleep(poll_interval)
                    continue
                raise

        raise Exception(f"Report did not complete within {max_wait_seconds} seconds")

    # ========== CONTEXT MANAGER SUPPORT ==========

    def __enter__(self):
        """Support for context manager (with statement)"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when exiting context manager"""
        self.close()
