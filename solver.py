
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Balle 2014

#
# Solver.py implements a single function
# responsible for the DPLL algorithm
#

import logic

# Solves the given CNF using the DPLL algorithm
#
# @param cnf : the CNF to be solved
# @param pure : whether to use Pure Elimination or not
# @param splits : number of total splits and unsuccesful splits
#
# @return whether cnf is satisfiable or not
#
def solve(cnf, pure, splits):

	# STEP 1a : Unit Propagation
	# -----
	# If a clause is a unit clause, i.e.
	# it contains only a single unassigned literal,
	# this clause can only be satisfied by assigning
	# the necessary value to make this literal true.
	count = cnf.unitPropagate()


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
		splits[1] += 1
		return False

	# STEP 2b :
	# -----
	# If the cnf contains no more clauses
	# then the CNF is satisfiable
	if cnf.isEmpty():

		# Print the solution
		print " Solution : \n-----------"
		print " satisfiable !"
		print " positive literals : (%d) " % len(cnf.solutions())
		print ', '.join(cnf.solutions())
		print
		return True

	# STEP 3 : Branching Step
	# -----
	# Select unassigned literal in CNF
	l = cnf.branch()
	splits[0] += 1


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
	return solve(cnft, pure, splits) or solve(cnf, pure, splits)



	