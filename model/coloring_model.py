
from gurobipy import Model

from model.abstract_model import AbstractModel


class ColoringModel(AbstractModel):
    def __init__(self, graph, config, upper_bound=None):
        self.graph = graph
        self.config = config
        self.name = config['model_name']
        self.m = Model(self.name)
        if upper_bound is None:
            self.upper_bound = len(self.graph.get_nodes())
        else:
            self.upper_bound = upper_bound
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
        return

    def _is_feasible(self):
        return

    def _process_infeasible_case(self):
        return

    def _post_process(self):
        # TODO get the stats of the model (e.g., runtime, gap.)
        return
