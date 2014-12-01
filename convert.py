
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import logic
import re

# CNF from String
# According to the DIMACS format used in SAT competitions
def generate(string, heuristic):

	# Step 0 : Sanitize and split into lines
	# Step 0a : replace multiple spaces by a single one
	clean = re.sub('[ ]+', ' ', string)

	# Step 0b : remove leading spaces and 0's indicating the end of a clause
	clean = re.sub('(^[ ]+|[ ]+0[ ]*)', '', clean, flags=re.MULTILINE)

	# Step 0c : split the string into lines and filter empty lines
	lines = filter(lambda l : l not in [' ',''] , clean.strip().split('\n'))

	# Step 1a : Get comments and info and display them to user
	comments = filter(lambda l : l[0] in ['p', 'c'], lines)
	if comments :
		print " Comments : \n=============="
		print '\n'.join(comments)
		print "=============="

	# Step 2 : Get the actual CNF
	cnf = lines[len(comments):]

	# Step 3 : create a variables for each absolute number
	# Step 3a : get absolute numbers
	snumbers = ' '.join(cnf).split(' ')
	numbers = map(lambda x : int(x), snumbers)
	absolutes = map(lambda x : abs(x), numbers)

	# Step 3b : create variables from absolute numbers
	variables = { i : logic.Var(i) for i in set(absolutes) }

	# Step 4 : create a literal for each number from the variables
	literals = { i : logic.Literal(variables[abs(i)], (i >= 0)) for i in set(numbers) }

	# Step 5 : create a clause for each line
	sclauses = [ x.split(' ') for x in cnf ]
	clauses = [ logic.Clause(map(lambda x : literals[int(x)], line)) for line in sclauses ]

	# Step 6 : display info to user
	print "CNF with %r variables and %r clauses " % (len(variables), len(clauses))

	# Step 7 : create CNF
	return logic.CNF(clauses,[], heuristic)
