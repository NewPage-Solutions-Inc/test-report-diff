import logging

from .default_formatter import DefaultDiffFormatter
from ..models.diff import TestResultDiff
from jinja2 import Template

logger = logging.getLogger(__name__)


class JinjiaFormatter(DefaultDiffFormatter):

    def __init__(self, diff: TestResultDiff):
        super().__init__(diff)

    def format(self) -> str:
        template = """
Old results: {{ diff.old_result.get_test_count() }}
{% for status, tests in diff.old_tests_by_status.items() -%}
{% if tests|length > 0 -%}
    {{ "\t" }}{{ status.name }}: {{ tests|length }}
{% endif -%}
{% endfor -%}
New results: {{ diff.new_result.get_test_count() }}
{% for status, tests in diff.new_tests_by_status.items() -%}
    {% if tests|length > 0 -%}
        {{ "\t" }}{{ status.name }}: {{ tests|length }}
{% endif -%}
{% endfor -%}
Diff:
{{ "\t" }}Newly Added Scenarios: {{ diff.newly_added_tests|length }}
{% for test in diff.newly_added_tests -%}
    {{ "\t\t" }}'{{ test.scenario_name }}'{{ " " }}
{% endfor -%}

{{ "\t" }}Newly Removed Scenarios: {{ diff.newly_removed_tests|length }}
{% for test in diff.newly_removed_tests -%}
    {{ "\t\t" }}'{{ test.scenario_name }}'{{ " " }}
{% endfor -%}

{% for status, tests in diff.tests_with_diff_status.items() -%}
    {% if tests|length > 0 -%}
        {{ "\t" }}Newly {{ status.name }}ed Scenarios: {{ tests|length }}
        {%- for test in tests -%}
            {{ "\n\t\t" }}'{{ test.scenario_name }}'
        {% endfor -%}
    {% endif -%}
{% endfor -%}
"""

        j2_template = Template(template)
        return j2_template.render({"diff": self._diff})
