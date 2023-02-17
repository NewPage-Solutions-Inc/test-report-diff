import xml.etree.ElementTree as ET
import logging

from ..models.status import TestStatus
from ..models.suite_result import TestSuiteResult
from ..models.test_result import TestResult

logger = logging.getLogger(__name__)


class PytestXmlProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.xml_data = ET.parse(f)

    def get_as_test_suite_result(self) -> TestSuiteResult:
        suite = TestSuiteResult()

        logger.debug(f"Parsing '{self.file_path}'")
        if len(self.xml_data.getroot()) == 0:
            return suite

        for xml_test_case in self.xml_data.getroot()[0]:
            xml_tc_attr = xml_test_case.attrib

            # capture details of the scenario
            test_result: TestResult = TestResult()

            test_result.feature_or_class_name = xml_tc_attr.get('classname')
            test_result.scenario_name = xml_tc_attr.get('name')
            logger.debug(f"Found scenario - '{test_result.scenario_name}'")

            test_result.status = TestStatus.PASS if len(xml_test_case) == 0 else TestStatus.FAIL
            test_result.duration_in_seconds = xml_tc_attr.get('time')

            if test_result.status == TestStatus.FAIL:
                failed_result = xml_test_case[0]
                test_result.error_trace = failed_result.text
                test_result.error_message = failed_result.attrib.get('message')

            logger.debug(f"Identified scenario status: {test_result.status}")
            logger.debug(f"Scenario duration: {test_result.duration_in_seconds}")
            suite.add_test_result(test_result)

        return suite
