import re

import pandas as pd

from util.util import add_output_cwd


class Analyzer(object):
    def __init__(self):
        columns = ['Instance', 'Model', 'Time', 'UB', 'LB', 'Gap', 'Presolve time', 'Root node time', 'Initial rows',
                   'Initial columns', 'Presolved rows', 'Presolved columns']
        self.result = {column: list() for column in columns}
        return

    def parse_log(self, log_name: str, key: str):
        """
        Analyze a gurobi log and get some key indicators.
        :param log_name:
        :param key:
        :return:
        """
        model = key.split('_')[0]
        instance = key.split('_')[1]
        with open(log_name, mode='r', encoding='utf-8') as f:
            text = f.readlines()
            text = ','.join(text)

            gap, lb, ub = self._get_obj_info(text)
            total_time = self._get_total_time(text)
            presolve_time = self._get_presolve_time(text)
            root_node_time = self._get_root_node(text)
            initial_columns, initial_rows = self._get_initial_size(text)
            presolved_columns, presolved_rows = self._get_presolved_size(text)

            self._add_record(instance, model, total_time, ub, lb, gap, presolve_time, root_node_time, initial_rows,
                             initial_columns, presolved_rows, presolved_columns)
        return

    def _get_presolved_size(self, text):
        presolved_prob_pattern = r'Presolved: (\d+) rows, (\d+) columns, (\d+) nonzeros'
        m = re.findall(presolved_prob_pattern, text)[-1]
        presolved_rows = m[0]
        presolved_columns = m[1]
        return presolved_columns, presolved_rows

    def _get_initial_size(self, text):
        initial_prob_pattern = r'Optimize a model with (\d+) rows, (\d+) columns and (\d+) nonzeros'
        m = re.findall(initial_prob_pattern, text)[-1]
        initial_rows = m[0]
        initial_columns = m[1]
        return initial_columns, initial_rows

    def _get_root_node(self, text):
        root_node_pattern = r'Root relaxation: objective (\d+\.\d+e\+\d+), (\d+) iterations, (\d+\.\d+) seconds'
        m = re.findall(root_node_pattern, text)
        if m:
            m = m[-1]
            lp_obj = m[0]
            simplex_iter = m[1]
            root_node_time = m[2]
            return root_node_time
        else:
            return None

    def _get_presolve_time(self, text):
        presolve_time_pattern = r'Presolve time: (\d+\.\d+)(s)'
        m = re.findall(presolve_time_pattern, text)[-1]
        presolve_time = m[0]
        return presolve_time

    def _get_total_time(self, text):
        time_pattern = r'Explored (\d+) nodes \((\d+) simplex iterations\) in (\d+\.\d+) seconds'
        m = re.findall(time_pattern, text)
        if m:
            m = m[-1]
            bb_nodes = m[0]
            simplex_iter = m[1]
            total_time = m[2]
            return total_time
        return None

    def _get_obj_info(self, text):
        obj_pattern = r'Best objective (\d+\.\d+e\+\d+), best bound (\d+\.\d+e\+\d+), gap (\d+\.\d+)\%'
        m = re.findall(obj_pattern, text)[-1]
        ub = m[0]
        lb = m[1]
        gap = m[2]
        return gap, lb, ub

    def _add_record(self, instance, model, total_time, ub, lb, gap, presolve_time, root_node_time, initial_rows,
                    initial_columns, presolved_rows, presolved_columns):
        self.result['Instance'].append(instance)
        self.result['Model'].append(model)
        self.result['Time'].append(total_time)
        self.result['UB'].append(ub)
        self.result['LB'].append(lb)
        self.result['Gap'].append(gap)
        self.result['Presolve time'].append(presolve_time)
        self.result['Root node time'].append(root_node_time)
        self.result['Initial rows'].append(initial_rows)
        self.result['Initial columns'].append(initial_columns)
        self.result['Presolved rows'].append(presolved_rows)
        self.result['Presolved columns'].append(presolved_columns)
        return

    def write_summary(self):
        df = pd.DataFrame(self.result)
        df.to_csv(add_output_cwd('result.csv'), index=False, encoding='utf-8-sig')
        return
