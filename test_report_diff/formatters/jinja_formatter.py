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
    <h4>Newly added scenarios: {{ newly_added_tests[0] }}</h4>
    <ul>
        {% for test in newly_added_tests[1] -%}
        <li>{{ test }}</li>
        {% endfor -%}
    </ul>

    <h4>Newly Removed Scenarios: {{ newly_removed_tests[0] }}</h4>
    <ul>
        {% for test in newly_removed_tests[1] -%}
        <li>{{ test }}</li>
        {% endfor -%}
    </ul>
{% for status, number_of_tests, tests in diff_status_items -%}
    <h4>Newly {{ status }}ed Scenarios: {{ number_of_tests }}</h4>
    <ul>
        {% for item in tests -%}
            <li>{{ item }}</li>
        {% endfor -%}
    </ul>
{% endfor -%}


    <script type="text/javascript">
var xValues = [
{% for result in old_result_content -%}
"{{ result[0] }}",
{% endfor -%}
];
var yValues = [
{% for result in old_result_content -%}
"{{ result[1] }}",
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
      text: "Old results: {{old_result_test_count}}"
    }
  }
});

var xValues = [
{% for result in new_result_content -%}
"{{ result[0] }}",
{% endfor -%}
];
var yValues = [
{% for result in new_result_content -%}
"{{ result[1] }}",
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
      text: "New results: {{new_result_test_count}}"
    }
  }
});
    </script>
</body>
</html>
"""
        j2_template = Template(template)
        return j2_template.render(self._get_data_to_render())

