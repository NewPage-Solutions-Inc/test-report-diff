"""Console script for test_report_diff."""
import sys
import click
import zipfile
import os

from test_report_diff.models.status import TestStatus
from test_report_diff.models.test_result import TestResult
from .formatters.triage_formatter import TriageFormatter
from .models.suite_result import TestSuiteResult
from .processors.cuke_json import CucumberJsonProcessor
from .models.diff import TestResultDiff


def unzip_file(file_path: str, destination: str = None):
    """Unzip the file if it is a zip file"""
    click.echo(f"Unzipping '{file_path}'")
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(destination)


def unzip_if_needed(dir_path):
    """if the path is a directory and it contains only zip files, then extract them"""
    if not os.path.isdir(dir_path):
        return

    files = os.listdir(dir_path)
    zip_files = [file for file in files if file.endswith('.zip')]
    if len(files) == len(zip_files):
        for file in files:
            unzip_file(os.path.join(dir_path, file), dir_path)


def export_fails_to_csv(file_name: str, results_by_status: dict[TestStatus, list[TestResult]]):
    count: int = 0
    with open(file_name, 'w') as csv_file:
        csv_file.write('Status,Feature,Scenario,Error\n')
        for status in [TestStatus.FAIL, TestStatus.SKIP, TestStatus.ERROR, TestStatus.UNKNOWN]:
            count += len(results_by_status[status])
            for test in results_by_status[status]:
                csv_file.write(f"{test.status.value},{test.feature_or_class_name},{test.scenario_name},{test.error_message}\n")

    click.echo(f"Exported {count} tests to '{file_name}'")


@click.command()
@click.argument('old_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.argument('new_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.option('-eo', '--export_old_fails', default='', type=click.Path(dir_okay=False))
@click.option('-en', '--export_new_fails', default='', type=click.Path(dir_okay=False))
def main(old_report_path: str, new_report_path: str, export_old_fails: str, export_new_fails: str):
    unzip_if_needed(old_report_path)
    unzip_if_needed(new_report_path)

    orig_results: TestSuiteResult = CucumberJsonProcessor(old_report_path).get_as_test_suite_result()
    new_results: TestSuiteResult = CucumberJsonProcessor(new_report_path).get_as_test_suite_result()

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    click.echo(TriageFormatter(diff).format())

    if export_old_fails:
        export_fails_to_csv(export_old_fails, diff.old_tests_by_status)

    if export_new_fails:
        export_fails_to_csv(export_new_fails, diff.new_tests_by_status)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
