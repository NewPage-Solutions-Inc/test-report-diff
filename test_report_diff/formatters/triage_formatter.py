import logging

from .default_formatter import DefaultDiffFormatter
from ..models.status import TestStatus
from ..models.test_result import TestResult
from ..models.diff import TestResultDiff

logger = logging.getLogger(__name__)


class TriageFormatter(DefaultDiffFormatter):

    def __init__(self, diff: TestResultDiff):
        super().__init__(diff)

    def _get_report_of_tests_with_diff_status(self) -> str:
        output: str = ""

        for status, tests in self._diff.tests_with_diff_status.items():
            num_of_tests: int = len(tests)
            logger.debug(f"Newly {status.name}ed tests - {num_of_tests}")
            if num_of_tests > 0:
                output += f"\n\t\tNewly {status.name}ed Scenarios: {num_of_tests}"
                output += "\n\t\t\t'" + "', '".join([test.scenario_name for test in tests]) + "'"
        return output

    @staticmethod
    def _get_report_from_list(label: str, results: list[TestResult]) -> str:
        output: str = ""

        num_tests: int = len(results)
        logger.debug(f"{label} - {num_tests}")
        if num_tests > 0:
            output += f"\n\t\t{label}: {num_tests}"
            output += f"""\n\t\t\t'{"', '".join([test.scenario_name for test in results])}'"""

        return output

    @staticmethod
    def _get_report_by_status(tests_by_status: dict[TestStatus, list[TestResult]]) -> str:
        output: str = ""

        for status, tests in tests_by_status.items():
            num_of_tests = len(tests)
            logger.debug(f"{status.value}ed tests - {num_of_tests}")
            if num_of_tests > 0:
                output += "\n\t\t" + f"{status.name}: {num_of_tests}"

        return output

    def format(self) -> str:
        logger.debug("Old results")
        formatted_diff = f"\n\tOld results: {self._diff.old_result.get_test_count()}"
        formatted_diff += self._get_report_by_status(self._diff.old_tests_by_status)

        logger.debug("New results")
        formatted_diff += f"\n\n\tNew results: {self._diff.new_result.get_test_count()}"
        formatted_diff += self._get_report_by_status(self._diff.new_tests_by_status)

        formatted_diff += "\n\n\tDiff:"
        formatted_diff += self._get_report_from_list("Newly Added Scenarios", self._diff.newly_added_tests)
        formatted_diff += self._get_report_from_list("Newly Removed Scenarios", self._diff.newly_removed_tests)
        formatted_diff += self._get_report_of_tests_with_diff_status()

        return formatted_diff
