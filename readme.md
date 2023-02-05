# Comparing Formulations of the Vertex Coloring Problem 

## What is it?

This is an implementation of the paper Jabrayilov and Mutzel (2023), which compares the MILP formulations of the vertex coloring problem, namely, the Assignment model, the POP (partial-ordering based) model, and the POPH (POP hybrid) model.

All models are the strengthened versions, along with some preprocessing tricks (e.g., an upper bound derived by a heuristic) mentioned in the paper.

## How to use it?

Run the `main.py` in the root directory. It will read instances defined in `config_local.yaml` (downloaded from https://mat.tepper.cmu.edu/COLOR/instances.html, standard graph coloring instances) and solve them via the Assign, POP, POPH models.

## Dependencies

This project depends on the [Gurobi solver](https://gurobi.com/) and [Networkx](https://networkx.org/) package.

## TODO List

- [X] Implement a max clique heuristic to find the initial lower bound of a graph (and add an associated constraint into the models).
  - It turns out that a greedy method performs poorly and I just use the method in `Networkx`.

- [X] Automatically analyze the Gurobi logs (via implementing a parser) and output the stat file. The official package `
grblogtools` is not available for Anaconda Python 3.6.

- [ ] Use the initial solution of the heuristic coloring method as a warm start of MILP models.

- [ ] Avoid defining redundant variables (i.e., g_{v, H}) in the POP and POPH models.

- [ ] Restructure and refactor.

- [X] Add functionality to draw the convergence plot (based on Gurobi log).


## Reference

Jabrayilov, A., Mutzel, P. 2023. Strengthened partial-ordering based ILP models for the vertex coloring problem. *Working Paper*.