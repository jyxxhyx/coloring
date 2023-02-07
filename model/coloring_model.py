
from gurobipy import Model

from model.abstract_model import AbstractModel
from util.util import add_logs_cwd


class ColoringModel(AbstractModel):
    def __init__(self, graph, config, upper_bound=None, lower_bound=None):
        self.graph = graph
        self.config = config
        self.name = config['model_name']
        self.log_file = config['log_file']
        self.m = Model(self.name)
        if upper_bound is None:
            self.upper_bound = len(self.graph.get_nodes())
        else:
            self.upper_bound = upper_bound
        if lower_bound:
            self.lower_bound = lower_bound
        else:
            self.lower_bound = None
        self.nodes = graph.get_nodes()
        self.edges = graph.get_edges()

    def _set_iterables(self):
        self.cap_h = list(range(self.upper_bound))
        return

    def _set_variables(self):
        return

    def _set_objective(self):
        return

    def _set_constraints(self):
        return

    def _optimize(self):
        # Print the name of the model in the log for further analysis.
        self.m.Params.log_file = self.log_file
        self.m.message('')
        self.m.message(self.name)
        self.m.Params.mip_gap = self.config['mip_gap']
        self.m.Params.time_limit = self.config['time_limit']
        self.m.optimize()
        return

    def _is_feasible(self):
        return

    def _process_infeasible_case(self):
        return

    def _post_process(self):
        # TODO get the stats of the model (e.g., runtime, gap.)
        return
