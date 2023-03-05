import json
import logging

from .status import TestStatus
from .suite_result import TestSuiteResult
from .test_result import TestResult

logger = logging.getLogger(__name__)


class TestResultDiff:

    def __init__(self, old_result: TestSuiteResult, new_result: TestSuiteResult):
        self.old_result: TestSuiteResult = old_result
        self.new_result: TestSuiteResult = new_result

        self.old_tests_by_status: dict[TestStatus, list[TestResult]] = {}
        self.new_tests_by_status: dict[TestStatus, list[TestResult]] = {}

        self.newly_added_tests: list[TestResult] = []
        self.newly_removed_tests: list[TestResult] = []

        self.tests_with_diff_status: dict[TestStatus, list[TestResult]] = {}

        self.existing_failures_with_diff_reason: list[TestResult] = []

    def __str__(self):
        """Return a json representation of the diff"""
        return json.dumps(self.__dict__)

    def calculate_diff(self):

        old_tests: dict[str, TestResult] = self.old_result.get_copy_as_test_results_map()
        new_tests: dict[str, TestResult] = self.new_result.get_copy_as_test_results_map()

        old_tests_set: set[TestResult] = set(old_tests.values())
        new_tests_set: set[TestResult] = set(new_tests.values())

        # region Create a map of tests by status for both old and new results

        # Initialize the maps
        for status in TestStatus:
            self.old_tests_by_status[status] = []
            self.new_tests_by_status[status] = []

        # Populate the map for the old tests
        for test in old_tests_set:
            self.old_tests_by_status[test.status].append(test)

        # Populate the map for the new tests
        for test in new_tests_set:
            self.new_tests_by_status[test.status].append(test)

        # endregion

        self.newly_added_tests = list(new_tests_set - old_tests_set)
        self.newly_removed_tests = list(old_tests_set - new_tests_set)

        common_tests = old_tests_set & new_tests_set  # Get the intersection of the two sets

        # Find old tests that have changed status in the latest run
        for status in TestStatus:
            self.tests_with_diff_status[status] = [test for test in common_tests
                                                   if new_tests[test.scenario_id].status == status
                                                   and old_tests[test.scenario_id].status != status]

        self.existing_failures_with_diff_reason = [test for test in common_tests
                                                   if TestStatus.FAIL == old_tests[test.scenario_id].status == new_tests[test.scenario_id].status
                                                   and new_tests[test.scenario_id].error_message != old_tests[test.scenario_id].error_message]
