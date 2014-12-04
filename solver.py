
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

#
# Solver.py implements a single function
# responsible for the DPLL algorithm
#

import logic

# Solves the given CNF using the DPLL algorithm
#
# @param cnf : the CNF to be solved
# @param pure : whether to use Pure Elimination or not
# @param failures : how many splits were unsuccesful
#
# @return whether cnf is satisfiable or not
#
def solve(cnf, pure, failures):

	# STEP 1a : Unit Propagation
	# -----
	# If a clause is a unit clause, i.e.
	# it contains only a single unassigned literal,
	# this clause can only be satisfied by assigning
	# the necessary value to make this literal true.
	cnf.unitPropagate()


	# STEP 1b : Pure Literal Elimination
	# -----
	# Pure literals can always be assigned in a way
	# that makes all clauses containing them true.
	# These clauses can be deleted.
	if pure:

		# Has significantly slowed down the algorithm
		# in pratice
		cnf.pureEliminate()
	

	# STEP 2a :
	# -----
	# If the cnf contains an empty clause
	# then the CNF is unsatisfiable
	if cnf.emptyClause():

		# Increment the number of failed splits
		failures[0] += 1
		return False

	# STEP 2b :
	# -----
	# If the cnf contains no more clauses
	# then the CNF is satisfiable
	if cnf.isEmpty():

		# Print the solution
		print " Solution : \n-----------"
		print " satisfiable !"
		print cnf.solutions()
		return True

	# STEP 3 : Branching Step
	# -----
	# Select unassigned literal in CNF
	l = cnf.branch()


	# STEP 4 :
	# -----
	# Create new CNF for new assignment
	# Then assign 
	cnft = cnf.copy()

	cnft.assign(l, True)
	cnf.assign(l, False)

	# STEP 5 : 
	# -----
	# Return the disjunction of the satisfiablility of both CNF's
	# Uses lazy evaluation
	return solve(cnft, pure, failures) or solve(cnf, pure, failures)



	