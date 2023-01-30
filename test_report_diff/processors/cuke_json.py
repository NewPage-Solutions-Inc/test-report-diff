import json
import logging
from typing import Any, Set

from ..models.status import TestStatus
from ..models.suite_result import TestSuiteResult
from ..models.test_result import TestResult

logger = logging.getLogger(__name__)


class CucumberJsonProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.json_data = json.load(f)

    @staticmethod
    def __get_from_json(obj, key: str, default=None) -> Any:
        if key in obj:
            return obj[key]
        else:
            # logger.debug(f"Key '{key}' not found. Returning default value '{default}' instead")
            return default

    def get_as_test_suite_result(self) -> TestSuiteResult:
        suite = TestSuiteResult()

        logger.debug(f"Parsing '{self.file_path}'")
        # for each feature in the json file
        for feature in self.json_data:
            # if the object is not a feature, skip it
            if not self.__get_from_json(feature, 'keyword') == 'Feature':
                continue

            # capture details of the feature
            feature_name = self.__get_from_json(feature, 'name')
            logger.debug(f"Found feature '{feature_name}'")
            feature_path = self.__get_from_json(feature, 'uri')
            feature_id = self.__get_from_json(feature, 'id')
            logger.debug(f"Feature ID: {feature_id}")

            tags_json = self.__get_from_json(feature, 'tags', [])
            feature_tags: Set = {tag['name'] for tag in tags_json}

            # for each scenario in the feature
            for scenario in self.__get_from_json(feature, 'elements', default=[]):
                # if the object is not a scenario, skip
                if not self.__get_from_json(scenario, 'keyword') == 'Scenario':
                    continue

                # capture details of the scenario
                test_result: TestResult = TestResult()

                test_result.feature_or_class_name = feature_name
                test_result.feature_or_test_file = feature_path if feature_path else feature_id
                test_result.scenario_id = self.__get_from_json(scenario, 'id')
                test_result.scenario_name = self.__get_from_json(scenario, 'name')
                logger.debug(f"Found scenario - '{test_result.scenario_name}'")
                logger.debug(f"Scenario ID - '{test_result.scenario_id}'")

                scenario_tags: Set = {tag['name'] for tag in self.__get_from_json(scenario, 'tags', [])}
                test_result.tags = list(feature_tags | scenario_tags)

                # by default, assume that the test has passed. Will be updated later if the test did not pass
                test_result.status = TestStatus.PASS

                last_passed_step: str = ''
                last_passed_step_line_num: int = 0
                scenario_duration: float = 0

                # for each step in the scenario
                for step in self.__get_from_json(scenario, 'steps', default=[]):
                    result = self.__get_from_json(step, 'result', default={})

                    status_str: str = self.__get_from_json(result, 'status', default='')
                    logger.debug(f"Actual step status: {status_str}")
                    status: TestStatus = TestStatus.from_string(status_str)
                    logger.debug(f"Identified step status: {status}")

                    step_text: str = self.__get_from_json(step, 'keyword', default='') + \
                                        self.__get_from_json(step, 'name', default='')
                    step_line_num: int = self.__get_from_json(step, 'line', default=0)

                    step_duration: int = self.__get_from_json(result, 'duration', default=0)
                    scenario_duration += (step_duration/1000000000)  # convert nanoseconds to seconds

                    # if the step had passed, capture the step info and move to the next step
                    if status == TestStatus.PASS:
                        last_passed_step = step_text
                        last_passed_step_line_num = step_line_num
                    else:
                        # if the step has any status other than pass, capture the step info and break
                        test_result.status = status

                        test_result.failed_step = step_text
                        test_result.failed_step_line_num = step_line_num

                        error_trace: str = self.__get_from_json(result, 'error_message', default=None)
                        test_result.error_trace = error_trace
                        test_result.error_message = error_trace.splitlines()[0] if error_trace else None

                        test_result.last_passed_step = last_passed_step
                        test_result.last_passed_step_line_num = last_passed_step_line_num

                        break

                test_result.duration_in_seconds = scenario_duration
                logger.debug(f"Identified scenario status: {test_result.status}")
                logger.debug(f"Scenario duration: {scenario_duration}")
                suite.add_test_result(test_result)

        return suite
