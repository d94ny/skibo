
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import random
import math
from collections import defaultdict

# ======== Helpers =========== #
# Helper functions for the heuristics

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

# ======= Heuristics ========= #

# First Occurence heuristic
def firstLiteral(cnf):
	return cnf.getLiterals()[0]
	
# Random heuristic
def randomLiteral(cnf):
	return random.choice(cnf.getLiterals())

# MOMS (Maximum Occurrence in clauses of Minimum Size) heuristic
def moms(cnf):

	# Step 1 : Find Clause with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : Find the literal with maximum occurence
	options = [ l for clause in minc for l in clause.literals ]

	# Count the occurences
	occurences = defaultdict(int)
	for literal in options:
		occurences[literal] += 1

	# Returns the maximum
	return max(occurences, key=occurences.get)

# MOMS alternative heuristic
# If f(x) the number of occurences of the variable x
# we choose the variable maximizing 
# [f(x) + f(\x)] * 2^k + [f(x) * f(\x)]
def momsf(cnf):

	# Step 0 : get k
	k = 2

	# Step 1 : Find Clauses with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : find f(x) and f(\x) for each x
	options = [ l for clause in minc for l in clause.literals ]

	# Make a dictonary containing (f(x), f(\x))
	occurences = defaultdict(lambda: [0,0])
	reference = {}

	for literal in options:

		# Check whether we increment f(x) or f(-x)
		index = 0 if literal.polarity else 1
		occurences[literal.variable][index] += 1

		# remember the corresponding literal (no matter the polarity)
		reference[literal.variable] = literal

	# Step 3 : comupte [f(x) + f(\x)] * 2k + [f(x) * f(\x)]
	values = { key : (v[0] + v[1])* math.pow(2,k) + (v[0]*v[1]) for key,v in occurences.items() }

	# Step 4 : get the maximum varibale
	var = max(values, key=values.get)

	# Step 5 : return one of the corresponding literal
	return reference[var]

# Freeman's POSIT version of MOMs
# Counts the positive x and negative x for each variable x
def posit(cnf):

	# Step 1 : Find Clauses with Minimum Size
	minc = minClauses(cnf.clauses)

	# Step 2 : 
	options = [ l for clause in minc for l in clause.literals ]

	occurences = defaultdict(int)
	reference = {}

	for l in options:

		occurences[l.variable] += 1
		reference[l.variable] = l

	# Return the maximum
	return reference[max(occurences, key=occurences.get)]


# Zabih and McAllester's version
# counts the negative occurrences only of each given variable x
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

# BOHM heuristic
# def bohm(cnf):
	
# 	bohmH = defaultdict(list)

# 	for clause in cnf.clauses:

# 		# Determine the length of the clause
# 		i = len(clause.literals)

# 		# For each literal in the clause, update his hi(x)
# 		for literal in clause:

# 			bohmH[literal.variable][]


# DLIS (Dynamic Largest Individual Sum) heuristic
# Choose the variable and value that satisfies the maximum number of unsatisfied clauses
#def dlis(cnf):
	# ...

# DLCS (Dynamic Largest Combined Sum) heuristic
# Count the number of clauses containing variable x
def dlcs(cnf):

	occurences = defaultdict(int)
	reference = {}

	for clause in cnf.clauses:

		for literal in clause.literals:
			occurences[literal.variable] += 1
			reference[literal.variable] = l

	return reference[max(occurences, key=occurences.get)]


# VSIDS (Variable State Independent Decaying Sum) heuristic
#def vsids(cnf):
	# ...

# Clause-Based heuristic
#def cbh(cnf):
	# ...


# Jeroslow-Wang heuristic
# for some literal compute J(l) = \sum{l in clause c} 2^{-|c|}
def jw(cnf):
	
	j = defaultdict(int)

	# Iterate over all clauses
	for clause in cnf.clauses:

		c = len(clause.literals)

		for l in clause.literals:
			j[l] += math.pow(2, -c)

	return max(j, key=j.get)



# Two Sided Jeroslow-Wang heuristic
def jw2(cnf):

	j = defaultdict(int)
	reference = {}

	# Iterate over all clauses
	for clause in cnf.clauses:

		c = len(clause.literals)

		for l in clause.literals:
			j[l.variable] += math.pow(2, -c)
			reference[l.variable] = l

	return reference[max(j, key=j.get)]


# Global variable with all heuristics
heuristics = { "firstLiteral": firstLiteral,
			   "randomLiteral": randomLiteral,
			   "moms": moms,
			   "momsf": momsf,
			   "posit": posit,
			   "jw": jw,
			   "jw2": jw2,
			   "dlcs": dlcs
			  }

