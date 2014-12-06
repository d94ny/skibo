
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Balle 2014

#
# Implements multiple branching heuristics
#

import random
import math
from collections import defaultdict

# ==== Global constants ====== #

k = 0

def setK(v):
	global k
	k = v

# ======== Helpers =========== #

# Returns the clauses with minimum size
def minClauses(clauses):
	minClauses = [];
	size = -1;

	for clause in clauses:

		clauseSize = len(clause.literals)

		# Either the current clause is smaller
		if size == -1 or clauseSize < size:
			minClauses = [clause]
			size = clauseSize

		# Or it is of minimum size as well
		elif clauseSize == size:
			minClauses.append(clause)

	return minClauses


# Literal Count Helper for :
# - Jeroslow-Wang heuristic
# - DLIS (Dynamic Largest Individual Sum) heuristic
# - MOMS heuristic
#
# Returns the literal maximizing each heuristics score
#
def literalCountHelper(clauses, id):

	# Assign a score to each literal
	score = defaultdict(int)

	# Iterate over all clauses
	for clause in clauses:

		# Determine by how much to increment the score
		# DLIS : +1 (occurrences)
		# MOMs : +1 (occurrences)
		# JW   : +2^{-|Clause|}
		incr = 1
		if id == "jw":
			incr = math.pow(2, -len(clause.literals))

		for l in clause.literals:
			score[l] += incr

	# Return the literal maximizing that score
	return max(score, key=score.get)



# Variable Count Helper for :
# - Two sided Jeroslow-Wang heuristic
# - DLCS (Dynamic Largest Combined Sum) heuristic
# - MOMSF heuristic
#
# Returns the variable maximizing each heuristics score
#
def variableCountHelper(clauses, id):

	# Get k for MOMSF
	global k

	# Assign two scores to each variable x :
	# 1 - one for the positive literal x
	# 2 - one for the negative literal -x
	# 
	# ex : [Cp and Cn]/[J(x) and J(-x)]/[f(x) and f(-x)]
	score = defaultdict(lambda: [0,0])

	# Remember the corresponding literal which we have to return
	# (i.e If we want to assign False to x return literal -x otherwise x)
	reference = {}

	# Iterate over all clauses
	for clause in clauses:

		# Determine by how much to increment the score
		# DLIS  : +1 (occurrences)
		# MOMSF : +1 (occurrences)
		# JW2   : +2^{-|Clause|}
		incr = 1
		if id == "jw2":
			incr = math.pow(2, -len(clause.literals))

		for literal in clause.literals:

			# Determine which score to increment (positive or negative)
			index = 0 if literal.polarity else 1
			score[literal.variable][index] += incr

			# Remember the corresponding literal
			reference[(literal.variable, literal.polarity)] = literal

	# Determine how to combine the score
	combined = {}

	if id == "momsf":
		# For momsf use [f(x) + f(-x)] * 2^k + [f(x) * f(-x)]
		combined = { key : (v[0] + v[1])* math.pow(2,k) + (v[0]*v[1]) for key,v in score.items() }

	else:
		# For jw2 and dlcs
		# use the combined value [Cp + Cn]/[J(x) + J(-x)]
		combined = { key : v[0] + v[1] for key,v in score.items() }

	# Get the variable maximizing this
	var = max(combined, key=combined.get)

	# Finally return x if [Cp >= Cn]/[J(x) >= J(-x)]/[f(x) >= f(-x)] otherwise -x
	polarity = True if score[var][0] >= score[var][1] else False
	return reference[(var, polarity)]



# ======= Heuristics ========= #

# HEURISTIC 1 :
# -----
# First Occurrence heuristic
# Simply returns the first literal in the list
def firstLiteral(cnf):
	return cnf.getLiterals()[0]
	

# HEURISTIC 2 :
# -----
# Random heuristic
# Returns a random heuristic
def randomLiteral(cnf):
	return random.choice(cnf.getLiterals())


# HEURISTIC 3 :
# -----
# MOMS (Maximum Occurrence in clauses of Minimum Size) heuristic
# Returns the literal with the most occurrences in all
# clauses of minimum size
def moms(cnf):

	# Step 1 : Find Clause with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : Find the literal with maximum occurrence
	return literalCountHelper(minc, "moms")


# HEURISTIC 4 :
# -----
# MOMS alternative heuristic
# If f(x) the number of occurrences of the variable x
# we choose the variable maximizing 
# [f(x) + f(-x)] * 2^k + [f(x) * f(-x)]
def momsf(cnf):

	# Step 1 : Find Clauses with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : Find the variable with maximum score [f(x) + f(-x)] * 2^k + [f(x) * f(-x)]
	return variableCountHelper(minc, "momsf")


# HEURISTIC 5 :
# -----
# Freeman's POSIT version of MOMs
# Counts the positive x and negative x for each variable x
def posit(cnf):

	# Step 1 : Find Clauses with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : Find the variable with maximum occurrence (like dlcs)
	return variableCountHelper(minc, "dlcs")


# HEURISTIC 6 :
# -----
# Zabih and McAllester's version of MOMs
# Counts the negative occurrences only of each given variable x
def ZM(cnf):

	# Step 1 : Find Clauses with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : 
	options = [ l for clause in minc for l in clause.literals ]

	occurences = defaultdict(int)
	reference = {}

	for l in options:

		if not l.polarity:
			occurences[l.variable] += 1
			reference[l.variable] = l

	# If no negative literal just return first option
	if len(occurences) == 0:
		return options[0]

	# Return the maximum
	return reference[max(occurences, key=occurences.get)]


# HEURISTIC 7 :
# -----
# DLCS (Dynamic Largest Combined Sum) heuristic
# Cp the number of clauses containing literal x 
# Cn the number of clauses containing literal -x
# 
# Here we select the variable maximizing Cp+Cn
# And return x if Cp > Cn otherwise -x
def dlcs(cnf):
	return variableCountHelper(cnf.clauses, "dlcs")


# HEURISTIC 8 :
# -----
# DLIS (Dynamic Largest Individual Sum) heuristic
# Choose the variable and value that satisfies the maximum number of unsatisfied clauses
# Like DLCS but we only consider the literal l (Thus Cp and Cn are individual)
def dlis(cnf):
	return literalCountHelper(cnf.clauses, "dlis")



# HEURISTIC 9 :
# -----
# Jeroslow-Wang heuristic
# For each literal compute J(l) = \sum{l in clause c} 2^{-|c|}
# Return the literal maximizing J
def jw(cnf):
	return literalCountHelper(cnf.clauses, "jw")


# HEURISTIC 10 :
# -----
# Two Sided Jeroslow-Wang heuristic
# Compute J(l) also counts the negation of l = J(x) + J(-x)
# We need to keep track of them separately
# as we return x if J(x) >= J(-x) otherwise -x
def jw2(cnf):
	return variableCountHelper(cnf.clauses, "jw2")


# ======== List =========== #

# Global variable with all heuristics
heuristics = { "firstLiteral": firstLiteral,
			   "randomLiteral": randomLiteral,
			   "moms": moms,
			   "momsf": momsf,
			   "posit": posit,
			   "jw": jw,
			   "jw2": jw2,
			   "dlcs": dlcs,
			   "dlis" : dlis,
			   "zm" : ZM
			  }

