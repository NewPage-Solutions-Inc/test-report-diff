"""Console script for test_report_diff."""
import sys
import click
import os

from .formatters.jinja_formatter import JinjiaFormatter
from .models.suite_result import TestSuiteResult
from .processors.cuke_json import CucumberJsonProcessor
from .models.diff import TestResultDiff


@click.command()
@click.argument('old_report_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.argument('new_report_path', required=True, type=click.Path(exists=True, dir_okay=False))
@click.option(
    '--html',
    is_flag=True,
    show_default=True,
    default=False,
    help='Render report as in html format. File fill be overwritten if exists'
)
def main(old_report_path: str, new_report_path: str, html: bool):
    orig_results: TestSuiteResult = CucumberJsonProcessor(old_report_path).get_as_test_suite_result()
    new_results: TestSuiteResult = CucumberJsonProcessor(new_report_path).get_as_test_suite_result()

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    click.echo(JinjiaFormatter(diff).format())

    if html:
        report_file_name = 'report_diff.html'
        if os.path.exists(report_file_name):
            click.echo(f'Warning: {report_file_name} will be overwritten!')
        with open(report_file_name, 'w') as f:
            f.write(JinjiaFormatter(diff).get_html_format())
        click.echo(f'Report diff is generated successfully.')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
