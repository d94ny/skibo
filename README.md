
# 15-354 Project - Simple SAT Solver
_Daniel Balle • dballe_

## Intro

This is a simple SAT solver written in Python based on the DPLL algorithm.

## Usage

	python main.py [file ...] [--heuristic ...] [--unit] [--pure] [--info] [--comments]


The `main.py` file requires a DIMACS CNF formatted file containing a formula in CNF form and will output whether it is satisfiable or not, providing a solution in the former case.

Additional arguments for `main.py` are :

* `--heuristic = ...` Specifies which branching heuristic the solver should use. See section *Heurisitcs* for a complete list of available heuristics and brief descriptions. Per default we use `firstLiteral`.
	
* `--pure` Uses Pure Elimination in the DPLL algorithm.

* `--unit` Uses Unit Propagation in the DPLL algorithm.

* `--info` Displays additional information such as number of literals and clauses, total number of branching splits and how many were unsuccessful, number of literals determined through unit propagation as well as pure elimination, and performance.

* `--comments` Displays comments from the DIMACS file if present.


## DIMACS CNF format

The algorithm requires the formula to be in Conjunctive Normal Form ([CNF](https://en.wikipedia.org/wiki/Conjunctive_normal_form)) using the DIMACS CNF format. According to [BASolver](http://logic.pdmi.ras.ru/~basolver/dimacs.html) this format is widely accepted as the standard format for boolean formulas in CNF.

	c
	c start with comments
	c 
	p cnf 5 3
	1 -5 4 0
	-1 5 3 4 0
	-3 -4 0


* Comments are lines starting with a `c`.
* Header information about the CNF containing the number of variables and clauses is a single line beginning with a `p`.
* Variables are integers greater or equal to 1.
* Literals are negative integers.
* Clauses are delimited either by a line break `\n` or a `0`. This SAT solver accepts either format.

You can find examples of DIMACS CNF files in the folder `cnf/`.

For more information please visit :

1. <http://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html>
2. <http://logic.pdmi.ras.ru/~basolver/dimacs.html>
3. <https://fairmut3x.wordpress.com/2011/07/29/cnf-conjunctive-normal-form-dimacs-format-explained/>


## Heuristics

This SAT solver implements the following branching heuristics which can be selected using the optional `--heuristic ...` argument:

* `firstLiteral` First Occurrence heuristic : simply selects the first literal in the formula.
 
* `randomLiteral` Random heuristic : selects a random literal in the formula

* `moms` Maximum Occurrence in clauses of Minimum Size heuristic : returns the literal with the most occurrences in all clauses of minimum size.
 
* `momsf` Variation of MOMS : If f(x) is the number of occurrences of the variable x in the clauses of minimum size, we return the variable maximizing (f(x) + f(-x)) * 2^k + (f(x) * f(-x))

* `posit` Freeman's POSIT version of MOMs : returns the variable with maximum occurrences in all clauses of minimum size.

* `zm` Zabih and McAllester's version of MOMs : returns the variable with maximum negative occurrences in all clauses of minimum size.

* `jw` Jeroslow-Wang heuristic : computes a score for each literal l based on the length of the clauses that contain it J(l) = \sum_{l \in C} 2^{-|C|}. Returns the literal maximizing that score.

* `jw2` Two-Sided Jeroslow-Wang heuristic : similar to the previous heuristic but computes the score for each variable x as J(x) + J(-x).

* `dlis` Dynamic Largest Individual Sum heuristic : returns the literal with the most occurrences in the formula.

* `dlcs` Dynamic Largest Combined Sum : returns the variables with the most occurrences in the formula.
