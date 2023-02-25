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
    help='Render report as in html format. File fill be overwritten if exists'
)
@click.option(
    '--template',
    type=click.Path(exists=True, dir_okay=False),
    help='Path to template to render with'
)
def main(old_report_path: str, new_report_path: str, template: str, html: str = None):
    orig_results: TestSuiteResult = CucumberJsonProcessor(old_report_path).get_as_test_suite_result()
    new_results: TestSuiteResult = CucumberJsonProcessor(new_report_path).get_as_test_suite_result()

    diff: TestResultDiff = TestResultDiff(orig_results, new_results)
    diff.calculate_diff()

    content = JinjiaFormatter(diff).get_html_format()
    try:
        if template:
            if not os.path.exists(template):
                raise FileNotFoundError
            with open(template, 'r') as f:
                content = JinjiaFormatter(diff).format(f.read())
    except FileNotFoundError:
        click.echo(f'Template file not found {template}')
    except:
        click.echo(f'Template contains syntax error')
    finally:
        click.echo(content)

    if html:
        if os.path.exists(html):
            click.echo(f'Warning: {html} will be overwritten!')
        with open(html, 'w') as f:
            f.write(JinjiaFormatter(diff).get_html_format())
        click.echo(f'Report diff is generated successfully.')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
