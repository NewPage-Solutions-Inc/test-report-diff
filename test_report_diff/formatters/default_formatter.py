from ..models.diff import TestResultDiff


class DefaultDiffFormatter:

    def __init__(self, diff: TestResultDiff):
        self._diff = diff

    def format(self):
        return str(self._diff)
