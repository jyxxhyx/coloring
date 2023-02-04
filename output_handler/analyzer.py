import re
from typing import Optional

import pandas as pd

from output_handler.plot import draw_iteration
from output_handler.regex_util import typeconvert_groupdict
from util.util import add_output_cwd, add_fig_cwd

float_pattern = r"[-+]?((\d*\.\d+)|(\d+\.?))([Ee][+-]?\d+)?"


class Analyzer(object):
    def __init__(self):
        columns = ['Instance', 'Model', 'Time', 'UB', 'LB', 'Gap', 'Presolve time', 'Root node time', 'Initial rows',
                   'Initial columns', 'Presolved rows', 'Presolved columns']
        self.result = {column: list() for column in columns}
        return

    def parse_log(self, log_name: str, model: str, instance: str, is_iteration_parsed: bool = False):
        """
        Analyze a gurobi log and get some key indicators.
        :param log_name: path of the log
        :param model: the associated model name
        :param instance: the associated instance name
        :param is_iteration_parsed: whether to parse the iteration info (if it exists)
        :return:
        """
        with open(log_name, mode='r', encoding='utf-8') as f:
            text = f.readlines()
            text = ','.join(text)

            gap, lb, ub = self._get_obj_info(text)
            total_time = self._get_total_time(text)
            root_node_time = self._get_root_node(text)
            initial_columns, initial_rows = self._get_initial_size(text)
            presolve_time, presolved_columns, presolved_rows = self._get_presolve_info(text)
            if is_iteration_parsed:
                df_iteration = self._get_iteration_info(text)
                draw_iteration(df_iteration, file_name=add_fig_cwd(f'{model}_{instance}.jpg'))

            self._add_record(instance, model, total_time, ub, lb, gap, presolve_time, root_node_time, initial_rows,
                             initial_columns, presolved_rows, presolved_columns)
        return

    def _get_presolve_info(self, text):
        """
        Get presolve related information.
        Note that there is an error in gurobi log.
        See the example below, the numbers of the rows and columns on the last line should be exchanged.
        ---
        Presolve time: 47.68s
        Presolved: 517637 rows, 18157 columns, 1581126 nonzeros
        Variable types: 0 continuous, 18157 integer (18157 binary)
        Found heuristic solution: objective 33.0000000

        Deterministic concurrent LP optimizer: primal and dual simplex
        Showing first log only...

        Presolved: 18157 rows, 535794 columns, 1599283 nonzeros
        ---
        :param text:
        :return:
        """
        presolved_prob_pattern = r'Presolve time: (\d+\.\d+)s\n,Presolved: (\d+) rows, (\d+) columns, (\d+) nonzeros'
        m = re.findall(presolved_prob_pattern, text)[-1]
        presolve_time = float(m[0])
        presolved_rows = int(m[1])
        presolved_columns = int(m[2])
        return presolve_time, presolved_columns, presolved_rows

    def _get_initial_size(self, text):
        initial_prob_pattern = r'Optimize a model with (\d+) rows, (\d+) columns and (\d+) nonzeros'
        m = re.findall(initial_prob_pattern, text)[-1]
        initial_rows = int(m[0])
        initial_columns = int(m[1])
        return initial_columns, initial_rows

    def _get_root_node(self, text):
        root_node_pattern = r'Root relaxation: objective (\d+\.\d+e\+\d+), (\d+) iterations, (\d+\.\d+) seconds'
        m = re.findall(root_node_pattern, text)
        if m:
            m = m[-1]
            lp_obj = m[0]
            simplex_iter = m[1]
            root_node_time = float(m[2])
            return root_node_time
        else:
            return None

    def _get_total_time(self, text):
        time_pattern = r'Explored (\d+) nodes \((\d+) simplex iterations\) in (\d+\.\d+) seconds'
        m = re.findall(time_pattern, text)
        if m:
            m = m[-1]
            bb_nodes = m[0]
            simplex_iter = m[1]
            total_time = float(m[2])
            return total_time
        return None

    def _get_obj_info(self, text):
        obj_pattern = r'Best objective (\d+\.\d+e\+\d+), best bound (\d+\.\d+e\+\d+), gap (\d+\.\d+)\%'
        m = re.findall(obj_pattern, text)[-1]
        ub = float(m[0])
        lb = float(m[1])
        gap = float(m[2])
        return gap, lb, ub

    def _get_iteration_info(self, text) -> Optional[pd.DataFrame]:
        # TODO get the final result
        progress = list()
        line_types = [
            # tree_search_full_log_line_regex
            re.compile(
                r'\s\s*(?P<CurrentNode>\d+)\s+(?P<RemainingNodes>\d+)\s+(?P<Obj>{0})\s+(?P<Depth>\d+)'
                r'\s+(?P<IntInf>\d+)\s+(?P<Incumbent>({0}|-))\s+(?P<BestBd>{0})\s+(?P<Gap>(-|{0}%))'
                r'\s+(?P<ItPerNode>({0}|-))\s+(?P<Time>\d+)s'.format(
                    float_pattern
                )
            ),
            # tree_search_nodepruned_line_regex
            re.compile(
                r'\s\s*(?P<CurrentNode>\d+)\s+(?P<RemainingNodes>\d+)\s+(?P<Pruned>(cutoff|infeasible|postponed))'
                r'\s+(?P<Depth>\d+)\s+(?P<Incumbent>(-|{0}))\s+(?P<BestBd>{0})\s+(?P<Gap>(-|{0}%))'
                r'\s+(?P<ItPerNode>({0}|-))\s+(?P<Time>\d+)s'.format(
                    float_pattern
                )
            ),
            # tree_search_new_solution_heuristic_log_line_regex
            re.compile(
                r'(?P<NewSolution>H)\s*(?P<CurrentNode>\d+)\s+(?P<RemainingNodes>\d+)\s+(?P<Incumbent>({0}|-))'
                r'\s+(?P<BestBd>{0})\s+(?P<Gap>{0}%)\s+(?P<ItPerNode>(-|{0}))\s+(?P<Time>\d+)s'.format(
                    float_pattern
                )
            ),
            # tree_search_new_solution_branching_log_line_regex
            re.compile(
                r'(?P<NewSolution>\*)\s*(?P<CurrentNode>\d+)\s+(?P<RemainingNodes>\d+)\s+(?P<Depth>\d+)'
                r'\s+(?P<Incumbent>({0}|-))\s+(?P<BestBd>{0})\s+(?P<Gap>{0}%)\s+(?P<ItPerNode>({0}|-))'
                r'\s+(?P<Time>\d+)s'.format(
                    float_pattern
                )
            ),
        ]
        last_iter_index = text.rfind('Expl')
        if last_iter_index:
            text = text[last_iter_index:].split('\n,')
            for line in text:
                for regex in line_types:
                    match = re.match(regex, line)
                    if match:
                        progress.append(typeconvert_groupdict(match))
                        break
            return pd.DataFrame(progress)
        else:
            return None

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
