from gurobipy import Model, quicksum, GRB

from model.coloring_model import ColoringModel


class PopModel(ColoringModel):
    def __init__(self, graph, config, upper_bound=None, lower_bound=None):
        super().__init__(graph, config, upper_bound, lower_bound)
        # TODO Choose the q node in a smart way.
        # self.q_node = self.nodes[0]
        self.q_node = self.graph.get_node_with_max_degree()
        self.largest_color = self.upper_bound - 1
        return

    def _set_iterables(self):
        super()._set_iterables()
        return

    def _set_variables(self):
        self.g = self.m.addVars(self.nodes,
                                self.cap_h,
                                vtype=GRB.BINARY,
                                name='g')
        return

    def _set_objective(self):
        self.m.setObjective(
            quicksum(self.g[self.q_node, i] for i in self.cap_h) + 1)
        return

    def _set_constraints(self):
        self.m.addConstrs((self.g[v, self.largest_color] == 0
                           for v in self.nodes),
                          name='fix-some-g')
        self.m.addConstrs((self.g[v, i - 1] - self.g[v, i] >= 0
                           for v in self.nodes
                           for i in self.cap_h if i >= 1),
                          name='linking')
        self.m.addConstrs(
            (self.g[u, 0] + self.g[v, 0] >= 2 - self.g[self.q_node, 0]
             for (u, v) in self.edges),
            name='edge1')
        self.m.addConstrs(
            (self.g[u, i - 1] - self.g[u, i] + self.g[v, i - 1] - self.g[v, i] <= self.g[self.q_node, i - 1]
             for (u, v) in self.edges
             for i in self.cap_h if i >= 1),
            name='edge2')
        self.m.addConstrs((self.g[self.q_node, i] - self.g[v, i] >= 0
                           for v in self.nodes
                           for i in self.cap_h),
                          name='upper_bound')
        self.m.addConstrs((self.g[self.q_node, i + 1] - self.g[v, i] >= 0
                           for v in self.graph.get_neighborhood(self.q_node)
                           for i in self.cap_h if i < self.largest_color),
                          name='strengthen')
        if self.lower_bound:
            self.m.addConstr(lhs=quicksum(self.g[self.q_node, i] for i in self.cap_h) + 1, sense=GRB.GREATER_EQUAL,
                             rhs=self.lower_bound, name='lb')
        return

    def _optimize(self):
        super()._optimize()
        return

    def _post_process(self):
        result = dict()
        for node in self.graph.get_nodes():
            for i in self.cap_h:
                if self.g[node, i + 1].x < 0.9:
                    result[node] = i
                    break
        return result

    def _is_feasible(self):
        return True

    def _process_infeasible_case(self):
        return dict()
