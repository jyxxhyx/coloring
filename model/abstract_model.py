from abc import ABC, abstractmethod


class AbstractModel(ABC):
    """
    We use the template method to define a generic class
    that defines the common procedures of optimization model
    """
    def solve(self):
        """
        The callable method of the class.
        :return:
        """
        self._set_iterables()
        self._set_variables()
        self._set_objective()
        self._set_constraints()
        self._optimize()
        if not self._is_feasible():
            return self._process_infeasible_case()
        else:
            return self._post_process()

    @abstractmethod
    def _set_iterables(self):
        """
        Define the sets used in the model.
        """
        pass

    @abstractmethod
    def _set_variables(self):
        """
        Define the decision variables.
        """
        pass

    @abstractmethod
    def _set_objective(self):
        """
        Define the objective function.
        """
        pass

    @abstractmethod
    def _set_constraints(self):
        """
        Define the constraints.
        """
        pass

    @abstractmethod
    def _optimize(self):
        """
        Solve the model.
        You might want to define the solver's parameters here
        and save the established model to disk.
        """
        pass

    @abstractmethod
    def _is_feasible(self):
        """
        Determine if the model is feasible.
        """
        pass

    @abstractmethod
    def _process_infeasible_case(self):
        """
        Handle the infeasible case.
        You might want to calculate the irreducible infeasible system (IIS) here.
        """
        pass

    @abstractmethod
    def _post_process(self):
        """
        Process the solution of the model
        and return a result stored in pure Python objects.
        """
        pass
