import json
from typing import List

from .status import TestStatus


class TestResult:

    def __init__(self):
        # For BDD/Gherkin tests, this would be the name of the feature and the path/file name of the feature file.
        # For pytest tests, this would be the name of the test module/class and the path/file name of the test file.
        self.feature_or_class_name: str = None
        self.feature_or_test_file: str = None

        self.scenario_id: str = None
        self.scenario_name: str = None
        self.tags: List[str] = []
        self.status: TestStatus = None
        self.duration_in_seconds: float = None

        self.error_message: str = None
        self.error_trace: str = None

        # Applicable only for Gherkin/BDD based tests
        self.failed_step: str = None
        self.failed_step_line_num: int = None
        self.last_successful_step: str = None
        self.last_successful_step_line_num: int = None

    def __str__(self):
        """Return a json representation of the diff"""
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        """If the feature_or_test_file and scenario_name are the same, then the test results are considered equal"""
        return isinstance(other, TestResult) and \
            self.feature_or_test_file == other.feature_or_test_file and \
            self.scenario_name == other.scenario_name and \
            self.scenario_id == other.scenario_id

    def __hash__(self):
        return hash(self.feature_or_test_file) \
               ^ hash(self.scenario_name) \
               ^ hash(self.scenario_id)
