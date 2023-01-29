from collections.abc import Callable

from .status import TestStatus
from .test_result import TestResult


class TestSuiteResult:
    def __init__(self, suite_info: str = None):
        self.__test_result_by_id: dict[str, TestResult] = {}
        self.suite_info: str = suite_info

    def get_test_count(self) -> int:
        return len(self.__test_result_by_id)

    def add_test_result(self, test_result: TestResult):
        self.__test_result_by_id[test_result.scenario_id] = test_result

    def get_copy_as_test_results_map(self) -> dict[str, TestResult]:
        return dict(self.__test_result_by_id)

    def get_result_for(self, scenario_id: str) -> TestResult:
        return self.__test_result_by_id.get(scenario_id)

    def get_test_results_matching(self, predicate: Callable[[TestResult], bool]) -> list[TestResult]:
        return [test_result for test_result in self.__test_result_by_id.values() if predicate(test_result)]

    def get_test_results_with_status(self, status: TestStatus) -> list[TestResult]:
        return self.get_test_results_matching(lambda result: result.status == status)

    def get_test_results_with_tag(self, tag: str) -> list[TestResult]:
        return self.get_test_results_matching(lambda result: tag in result.tags)
