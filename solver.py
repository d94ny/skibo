
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import logic

# Main function
# Solves only CNF for now
def solve(cnf):

	# STEP 1a : Unit Propagation
	# If a clause is a unit clause, i.e.
	# it contains only a single unassigned literal,
	# this clause can only be satisfied by assigning
	# the necessary value to make this literal true
	cnf.unitPropagate()

	# STEP 1b : Pure literal elimination
	# Pure literals can always be assigned in a way
	# that makes all clauses containing them true.
	# These clauses can be deleted
	# cnf.pureEliminate()
	# Can make it much slower

	# STEP 2a :
	# If cnf contains an empty clause
	# then the CNF is unsatisfiable
	if cnf.emptyClause():
		# print "Instance fail"
		return False

	# STEP 2b :
	# If the cnf contains no more clauses
	# then the CNF is satisfiable
	if cnf.isEmpty():
		print cnf.solutions()
		return True

	# STEP 3 : Branching Step
	# Select unassigned literal in CNF
	l = cnf.branch()
	# For bebugging 
	# print "Branching on ", l

	# STEP 4 : Create new CNF for new assignment
	cnft = cnf.copy()

	cnft.assign(l, True)
	cnf.assign(l, False)

	# STEP 5 : Split with 2 copies of CNF
	return solve(cnft) or solve(cnf)



	