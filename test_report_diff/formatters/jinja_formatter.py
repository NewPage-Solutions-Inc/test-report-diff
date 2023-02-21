import logging

from .default_formatter import DefaultDiffFormatter
from ..models.diff import TestResultDiff
from jinja2 import Template

logger = logging.getLogger(__name__)


class JinjiaFormatter(DefaultDiffFormatter):

    def __init__(self, diff: TestResultDiff):
        super().__init__(diff)

    def _get_data_to_render(self):
        return {
            "old_result_test_count": self._diff.old_result.get_test_count(),
            "old_result_content": [
                (status.name, len(tests)) for status, tests in self._diff.old_tests_by_status.items() if len(tests) > 0
            ],
            "new_result_test_count": self._diff.new_result.get_test_count(),
            "new_result_content": [
                (status.name, len(tests)) for status, tests in self._diff.new_tests_by_status.items() if len(tests) > 0
            ],
            "newly_added_tests": (
                len(self._diff.newly_added_tests),
                [test.scenario_name for test in self._diff.newly_added_tests]
            ),
            "newly_removed_tests": (
                len(self._diff.newly_removed_tests),
                [test.scenario_name for test in self._diff.newly_removed_tests]
            ),
            "diff_status_items": [
                (
                    status.name,
                    len(tests),
                    [test.scenario_name for test in tests]
                ) for status, tests in self._diff.tests_with_diff_status.items() if len(tests) > 0
            ]
        }

    def format(self) -> str:
        template = """
Old results: {{old_result_test_count}}
{% for result in old_result_content -%}
{{ "\t" }}{{ result[0] }}: {{ result[1] }}
{% endfor -%}

New results: {{new_result_test_count}}
{% for result in new_result_content -%}
{{ "\t" }}{{ result[0] }}: {{ result[1] }}
{% endfor -%}

Diff:
{{ "\t" }}Newly Added Scenarios: {{ newly_added_tests[0] }}
{% for test in newly_added_tests[1] -%}
{{ "\t\t" }}'{{ test }}'{{ " " }}
{% endfor -%}

{{ "\t" }}Newly Removed Scenarios: {{ newly_removed_tests[0] }}
{% for test in newly_removed_tests[1] -%}
{{ "\t\t" }}'{{ test }}'{{ " " }}
{% endfor -%}

{% for status, number_of_tests, tests in diff_status_items -%}
    {{ "\t" }}Newly {{ status }}ed Scenarios: {{ number_of_tests }}
    {% for item in tests -%}
        {{ "\t\t" }}'{{ item }}'
    {% endfor -%}
{% endfor -%}
"""

        j2_template = Template(template)
        return j2_template.render(self._get_data_to_render())
