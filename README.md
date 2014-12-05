
# 15-354 Project - Simple SAT Solver
_Daniel Balle • dballe_

## Intro

This is a simple SAT solver written in Python based on the DPLL algorithm.

## Usage

	python main.py [file ...] [--heuristic=...] [--info] [--comments] [--help] [--pure]


The `main.py` file requires a DIMACS CNF formatted file containing a formula in CNF form and will output whether it is satisfiable or not, providing a solution in the former case.

Additional arguments are :

* `--heuristic = ...` Specifies which branching heuristic the solver should use. See section **Heurisitcs** for a complete list of available heuristics and brief descriptions.
The default heuristic is `firstLiteral`.

* `--info` Displays additional information such as number of literals and clauses, total number of branching splits and how many were unsuccessful, number of units propagated and performance.

* `--comments` Displays comments from the DIMACS file if present.

* `--pure` uses Pure Elimination in the DPLL algorithm, off by default.


## DIMACS CNF format


## Heuristics

## Files