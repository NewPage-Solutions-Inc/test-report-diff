"""Console script for test_report_diff."""
import sys
import click

from .formatters.triage_formatter import TriageFormatter
from .models.suite_result import TestSuiteResult
from .processors.cuke_json import CucumberJsonProcessor
from .processors.allure_json import AllureJsonProcessor
from .models.diff import TestResultDiff


@click.command()
@click.argument('old_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.argument('new_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.argument('report_type', default='cucumber', type=str)
def main(old_report_path: str, new_report_path: str, report_type: str):
    if report_type == 'cucumber':
        orig_results: TestSuiteResult = CucumberJsonProcessor(old_report_path).get_as_test_suite_result()
        new_results: TestSuiteResult = CucumberJsonProcessor(new_report_path).get_as_test_suite_result()
    elif report_type == 'allure':
        orig_results: TestSuiteResult = AllureJsonProcessor(old_report_path).get_as_test_suite_result()
        new_results: TestSuiteResult = AllureJsonProcessor(new_report_path).get_as_test_suite_result()
    else:
        click.echo(f"Unsupported report type '{report_type}'")
        return 1

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    click.echo(TriageFormatter(diff).format())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
