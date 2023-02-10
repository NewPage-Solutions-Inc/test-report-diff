import json
import logging
import os
import glob
from ..models.status import TestStatus
from ..models.suite_result import TestSuiteResult
from ..models.test_result import TestResult

logger = logging.getLogger(__name__)


class AllureJsonProcessor:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = list(
            filter(os.path.isfile, glob.glob(f"{dir_path}/*.json"))
        )

    def get_as_test_suite_result(self) -> TestSuiteResult:
        suite = TestSuiteResult()
        logger.debug(f"Parsing '{self.dir_path}'")
        for a_file in self.files:
            with open(os.path.join(self.dir_path, a_file), 'r') as f:
                suite.add_test_result(self.get_scenario_data(json.load(f)))

        return suite

    def get_scenario_data(self, raw_data: json) -> TestResult:
        test_result: TestResult = TestResult()
        test_result.feature_or_class_name = raw_data.get('labels', [{}])[0].get('name')
        test_result.feature_or_test_file = raw_data.get('fullName')
        test_result.scenario_id = raw_data.get('uuid')
        test_result.scenario_name = raw_data.get('name')
        logger.debug(f"Found scenario - '{test_result.scenario_name}'")
        logger.debug(f"Scenario ID - '{test_result.scenario_id}'")

        test_result.tags = []

        try:
            test_status = TestStatus(raw_data.get('status').upper())
        except ValueError:
            test_status = TestStatus.UNKNOWN

        test_result.status = test_status
        failed_step = ''
        if test_status != TestStatus.PASS:
            for step in raw_data.get('steps'):
                if step.get('status') != 'passed':
                    failed_step = step.get('name')
                    break

        test_result.failed_step = failed_step
        test_result.error_trace = raw_data.get('statusDetails', {}).get('trace')
        test_result.error_message = raw_data.get('statusDetails', {}).get('message')

        test_start = raw_data.get('start')
        test_stop = raw_data.get('stop')

        test_duration: float = (test_stop - test_start)/1000

        test_result.duration_in_seconds = test_duration
        logger.debug(f"Identified scenario status: {test_result.status}")
        logger.debug(f"Scenario duration: {test_duration}")
        return test_result
