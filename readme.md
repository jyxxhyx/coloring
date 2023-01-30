# Comparing Formulations of the Vertex Coloring Problem 

## What is it?

This is an implementation of the paper Jabrayilov and Mutzel (2023), which compares the MILP formulations of the vertex coloring problem, namely, the Assignment model, the POP (partial-ordering based) model, and the POPH (POP hybrid) model.

All models are the strengthened versions, along with some the preprocessing tricks (e.g., an upper bound derived by a heuristic) mentioned in the paper.

## How to use it?

Run the `main.py` in the root directory. It will read instances defined in `config_local.yaml` (downloaded from https://mat.tepper.cmu.edu/COLOR/instances.html, standard graph coloring instances) and solve them via the Assign, POP, POPH models.

## TODO List

- Implement a max clique heuristic to find the initial lower bound of a graph (and maybe add an associated constraint into the models).

- Automatically analyze the Gurobi logs (via implementing a parser manually or using the official package `
grblogtools`) and output the stat file.

- Restructure and refactor.


## Reference

Jabrayilov, A., Mutzel, P. 2023. Strengthened partial-ordering based ILP models for the vertex coloring problem. *Working Paper*.