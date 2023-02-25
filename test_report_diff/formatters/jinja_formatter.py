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

    def get_html_format(self):
        template = """
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Test Report Diff</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
</head>
<body>
    <table style="width: 100%">
        <tr>
            <td style="width: 50%">
                <canvas id="old_result" style=""></canvas>
            </td>
            <td>
                <canvas id="new_result"></canvas>
            </td>
        </tr>
    </table>
    <br>
    <h3>Diff:</h3>
    <h4>Newly added scenarios: {{ diff.newly_added_tests|length }}</h4>
    <ul>
        {% for test in diff.newly_added_tests -%}
        <li>{{ test.scenario_name }}</li>
        {% endfor -%}
    </ul>

    <h4>Newly Removed Scenarios: {{ diff.newly_removed_tests|length }}</h4>
    <ul>
        {% for test in diff.newly_removed_tests -%}
        <li>{{ test.scenario_name }}</li>
        {% endfor -%}
    </ul>
{% for status, tests in diff.tests_with_diff_status.items() -%}
    <h4>Newly {{ status.name }}ed Scenarios: {{ tests|length }}</h4>
    <ul>
        {% for test in tests -%}
            <li>{{ test.scenario_name }}</li>
                <details>
                <ul>
                    {% if test.duration_in_seconds is not none %} <li>Duration: {{ test.duration_in_seconds }}s</li> {% endif %}
                    {% if test.error_message is not none %} <li>Error message: {{ test.error_message }}</li> {% endif %}
                    {% if test.error_trace is not none %} <li>Error message: {{ test.error_trace }}</li> {% endif %}
                    {% if test.failed_step is not none %} <li>Error Trace: {{ test.failed_step }}</li> {% endif %}
                    {% if test.failed_step is not none %} <li>Failed step: {{ test.failed_step }}</li> {% endif %}
                    {% if test.failed_step_line_num is not none %} <li>Failed line number: {{ test.failed_step_line_num }}</li> {% endif %}
                    {% if test.last_successful_step is not none %} <li>Last successful step: {{ test.last_successful_step }}</li> {% endif %}
                    {% if test.last_successful_step_line_num is not none %} <li>Last successful line number: {{ test.last_successful_step_line_num }}</li> {% endif %}
                </ul>
                </details>
        {% endfor -%}
    </ul>
{% endfor -%}


    <script type="text/javascript">
var xValues = [
{% for status, tests in diff.old_tests_by_status.items() -%}
{% if tests|length > 0 -%}
"{{ status.name }}",
{% endif -%}
{% endfor -%}
];
var yValues = [
{% for status, tests in diff.old_tests_by_status.items() -%}
{% if tests|length > 0 -%}
"{{ tests|length }}",
{% endif -%}
{% endfor -%}
];

new Chart("old_result", {
  type: "pie",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: color => {
                        var r = Math.floor(Math.random() * 255);
                        var g = Math.floor(Math.random() * 255);
                        var b = Math.floor(Math.random() * 255);
                        return "rgba(" + r + "," + g + "," + b + ", 0.5)";
                    },
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "Old results: {{ diff.old_result.get_test_count() }}"
    }
  }
});

var xValues = [
{% for status, tests in diff.new_tests_by_status.items() -%}
{% if tests|length > 0 -%}
"{{ status.name }}",
{% endif -%}
{% endfor -%}
];
var yValues = [
{% for status, tests in diff.new_tests_by_status.items() -%}
{% if tests|length > 0 -%}
"{{ tests|length }}",
{% endif -%}
{% endfor -%}
];

new Chart("new_result", {
  type: "pie",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: color => {
                        var r = Math.floor(Math.random() * 255);
                        var g = Math.floor(Math.random() * 255);
                        var b = Math.floor(Math.random() * 255);
                        return "rgba(" + r + "," + g + "," + b + ", 0.5)";
                    },
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      text: "New results: {{ diff.new_result.get_test_count() }}"
    }
  }
});
    </script>
</body>
</html>
"""
        j2_template = Template(template)
        return j2_template.render({"diff": self._diff})

