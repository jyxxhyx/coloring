import re
from unittest import TestCase

from output_handler.analyzer import Analyzer
from util.util import add_logs_cwd


class TestAnalyzer(TestCase):
    def test_parse_log(self):
        analyzer = Analyzer()
        log_file = 'poph_games120.col.log'
        key = 'poph_games120'
        analyzer.parse_log(add_logs_cwd(log_file), key)
        print(analyzer.result)

    def test__get_presolve_time(self):
        analyzer = Analyzer()
        text = 'Presolve time: 0.23s'
        presolve_time = analyzer._get_presolve_time(text)
        print(presolve_time)

    def test_re(self):
        text = 'Best objective 9.000000000000e+00, best bound 9.000000000000e+00, gap 0.0000%, Best objective ' \
               '8.000000000000e+00, best bound 7.000000000000e+00, gap 1.0000%'
        obj_pattern = r'Best objective (\d+\.\d+e\+\d+), best bound (\d+\.\d+e\+\d+), gap (\d+\.\d+)\%'
        m = re.findall(obj_pattern, text)[-1]
        ub = m[0]
        lb = m[1]
        gap = m[2]
        print(f'{ub},{lb},{gap}')
