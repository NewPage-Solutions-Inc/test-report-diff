"""Console script for test_report_diff."""
import sys
import click

from .formatters.triage_formatter import TriageFormatter
from .models.suite_result import TestSuiteResult
from .processors.cuke_json import CucumberJsonProcessor
from .models.diff import TestResultDiff


@click.command()
@click.argument('old_report_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('new_report_path', required=True, type=click.Path(exists=True, dir_okay=False))
def main(old_report_path: str, new_report_path: str):
    orig_results: TestSuiteResult = CucumberJsonProcessor(old_report_path).get_as_test_suite_result()
    new_results: TestSuiteResult = CucumberJsonProcessor(new_report_path).get_as_test_suite_result()

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    click.echo(TriageFormatter(diff).format())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
