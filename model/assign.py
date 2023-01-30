from gurobipy import Model, quicksum, GRB

from model.coloring_model import ColoringModel


class AssignModel(ColoringModel):
    def __init__(self, graph, config, upper_bound=None):
        super().__init__(graph, config, upper_bound)
        return

    def _set_iterables(self):
        super()._set_iterables()
        return

    def _set_variables(self):
        self.x = self.m.addVars(self.nodes, self.cap_h,
                                vtype=GRB.BINARY,
                                name='x')
        self.w = self.m.addVars(self.cap_h, vtype=GRB.BINARY, name='w')
        return

    def _set_objective(self):
        self.m.setObjective(quicksum(self.w[i] for i in self.cap_h))
        return

    def _set_constraints(self):
        self.m.addConstrs((quicksum(self.x[v, i] for i in self.cap_h) == 1
                           for v in self.nodes),
                          name='assign')
        self.m.addConstrs((self.x[v, i] + self.x[u, i] <= self.w[i]
                           for i in self.cap_h
                           for (u, v) in self.edges),
                          name='edge')
        self.m.addConstrs(
            (self.w[i] <= quicksum(self.x[v, i]
                                   for v in self.nodes)
             for i in self.cap_h),
            name='linking')
        self.m.addConstrs(
            (self.w[i] <= self.w[i - 1] for i in self.cap_h if i >= 1),
            name='symmetry-breaking')
        return

    def _optimize(self):
        self.m.Params.mip_gap = self.config['mip_gap']
        self.m.Params.time_limit = self.config['time_limit']
        self.m.write(f'{self.name}.lp')
        self.m.optimize()
        return

    def _post_process(self):
        result = dict()
        for node in self.nodes:
            for i in self.cap_h:
                if self.x[node, i].x > 0.9:
                    result[node] = i
                    break
        return result

    def _is_feasible(self):
        return True

    def _process_infeasible_case(self):
        return dict()
