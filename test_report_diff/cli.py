"""Console script for test_report_diff."""
import sys
import click
from .formatters.triage_formatter import TriageFormatter
from .models.suite_result import TestSuiteResult
from .models.diff import TestResultDiff
from . import util


@click.command()
@click.argument('old_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.argument('new_report_path', required=True, type=click.Path(exists=True, dir_okay=True))
@click.argument('report_type', default='cucumber', type=str)
def main(old_report_path: str, new_report_path: str, report_type: str) -> int:
    processor_cls = util.get_processor_class_by_report_type(
        report_type,
        util.get_processors()
    )

    if processor_cls is None:
        click.echo(f"Unsupported report type '{report_type}'")
        return 0

    orig_results: TestSuiteResult = processor_cls(old_report_path).get_as_test_suite_result()
    new_results: TestSuiteResult = processor_cls(new_report_path).get_as_test_suite_result()

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    click.echo(TriageFormatter(diff).format())

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
