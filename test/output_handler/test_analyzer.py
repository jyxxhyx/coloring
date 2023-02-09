import re
from unittest import TestCase

from output_handler.analyzer import GurobiAnalyzer
from util.util import add_logs_cwd


class TestAnalyzer(TestCase):
    def setUp(self):
        """
        The fixture equivalent in unittest package
        :return:
        """
        self.analyzer = GurobiAnalyzer('result.csv')
        return

    def test_parse_log(self):
        log_file = 'test.log.test'
        model = 'poph'
        instance = 'game120'
        self.analyzer.parse_log(add_logs_cwd(log_file), model, instance)
        print(self.analyzer.result)
        self.assertEqual(self.analyzer.result['Presolved rows'][0], 2386)
        self.assertEqual(self.analyzer.result['Presolved columns'][0], 1178)
        self.assertEqual(self.analyzer.result['Initial rows'][0], 9018)
        self.assertEqual(self.analyzer.result['Initial columns'][0], 2400)
        self.assertAlmostEqual(self.analyzer.result['Time'][0], 0.14)
        self.assertAlmostEqual(self.analyzer.result['UB'][0], 9.0)
        self.assertAlmostEqual(self.analyzer.result['LB'][0], 9.0)
        self.assertAlmostEqual(self.analyzer.result['Gap'][0], 0.0)
        self.assertAlmostEqual(self.analyzer.result['Presolve time'][0], 0.11)
        self.assertAlmostEqual(self.analyzer.result['Root node time'][0], 0.01)

    def test__get_presolve_info(self):
        text = 'Presolve time: 47.68s\n,Presolved: 517637 rows, 18157 columns, 1581126 nonzeros'
        result = self.analyzer._get_presolve_info(text)
        print(result)
        self.assertAlmostEqual(result[0], 47.68)
        self.assertEqual(result[1], 517637)
        self.assertEqual(result[2], 18157)

    def test_re(self):
        text = 'Best objective 9.000000000000e+00, best bound 9.000000000000e+00, gap 0.0000%, Best objective ' \
               '8.000000000000e+00, best bound 7.000000000000e+00, gap 1.0000%'
        obj_pattern = r'Best objective (\d+\.\d+e\+\d+), best bound (\d+\.\d+e\+\d+), gap (\d+\.\d+)\%'
        m = re.findall(obj_pattern, text)[-1]
        ub = float(m[0])
        lb = float(m[1])
        gap = float(m[2])
        print(f'{ub},{lb},{gap}')
        self.assertAlmostEqual(ub, 8.0)
        self.assertAlmostEqual(lb, 7.0)
        self.assertAlmostEqual(gap, 1.0)

    def test__get_iteration_info(self):
        text = ' Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time\n,\n,' \
               'H    0     0                       9.0000000    9.00000  0.00%     -    0s\n,' \
               '     0     0    9.00000    0  155    9.00000    9.00000  0.00%     -    0s\n,'
        result = self.analyzer._get_iteration_info(text)
        print(result)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result.at[1, 'IntInf'], 155.0)
