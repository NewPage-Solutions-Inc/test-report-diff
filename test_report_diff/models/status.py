from enum import Enum

_pass_synonyms = ['PASS', 'PASSED', 'OK', 'SUCCESS', 'P']
_fail_synonyms = ['FAIL', 'FAILED', 'FAILURE', 'F']
_xfail_synonyms = ['XFAIL', 'XFAILED', 'XFAILURE']
_skip_synonyms = ['SKIP', 'SKIPPED']
_error_synonyms = ['ERROR', 'ERR', 'EXCEPTION', 'E']
_unknown_synonyms = ['UNKNOWN', 'UNDEFINED', 'NULL', 'U', '']


class TestStatus(Enum):
    """Test status enum."""
    PASS = 'PASS'
    FAIL = 'FAIL'
    XFAIL = 'XFAIL'
    SKIP = 'SKIPPED'
    ERROR = 'ERROR'
    UNKNOWN = 'UNKNOWN'

    @staticmethod
    def from_string(status: str):
        """Get status from string. Matches with synonyms for the status as well."""
        tmp_status: str = status.strip().upper()
        if tmp_status in _pass_synonyms:
            return TestStatus.PASS
        elif tmp_status in _fail_synonyms:
            return TestStatus.FAIL
        elif tmp_status in _xfail_synonyms:
            return TestStatus.XFAIL
        elif tmp_status in _skip_synonyms:
            return TestStatus.SKIP
        elif tmp_status in _error_synonyms:
            return TestStatus.ERROR
        else:
            return TestStatus.UNKNOWN
