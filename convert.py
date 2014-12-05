
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Balle 2014

#
# Converts a file or string to a CNF
#

import logic
import re

# Generates a CNF from a string according
# to the DIMACS format used in SAT competitions
#
# @param string : input CNF in classic DIMACS format
# @param heuristic : heuristic to be used for the branching step
# @param showInfo : whether to show additional info
# @param showComments : whether to show string comments
#
# @return whether cnf is satisfiable or not
#
def generate(string, heuristic, showInfo, showComments):

	# STEP 0 :
	# -----
	# Sanitize
	# Either using 0's or line breaks

	# replace multiple spaces by a single one
	clean = re.sub('[ ]+', ' ', string)

	# remove leading spaces
	clean = re.sub('^[ ]+', '', clean, flags=re.MULTILINE)

	# split the string into lines and filter empty lines
	lines = filter(lambda l : l not in [' ',''] , clean.strip().split('\n'))


	# STEP 1 :
	# -----
	# Get comments and info and display them to user
	comments = filter(lambda l : l[0] in ['p', 'c'], lines)
	if comments and showComments :
		print " Comments : \n-----------"
		print '\n'.join(map(lambda x : ' ' + x[1:].strip(), comments))
		print 


	# STEP 2 :
	# -----
	# Get the actual CNF
	cnf = lines[len(comments):]


	# STEP 3 :
	# -----
	# Split into clauses
	# Either using the 0 character or line breaks (search in clean)
	if re.search('[ ]+0[ ]*', clean):
		
		# 0's are used for the end of clause rather than \n
		cnf = ' '.join(cnf)
		cnf = re.sub('[ ]+0[ ]*','\n', cnf)
		cnf = filter(lambda l : l not in [' ',''] , cnf.strip().split('\n'))


	# STEP 4 :
	# -----
	# create a variables for each absolute number
	
	# get absolute numbers
	snumbers = ' '.join(cnf).split(' ')
	numbers = map(lambda x : int(x), snumbers)
	absolutes = map(lambda x : abs(x), numbers)

	# create variables from absolute numbers
	variables = { i : logic.Var(i) for i in set(absolutes) }


	# STEP 5 :
	# -----
	# create a literal for each number from the variables
	literals = { i : logic.Literal(variables[abs(i)], (i >= 0)) for i in set(numbers) }


	# STEP 6 :
	# -----
	# create a clause for each line
	sclauses = [ x.split(' ') for x in cnf ]
	clauses = [ logic.Clause(map(lambda x : literals[int(x)], line)) for line in sclauses ]


	# STEP 7 :
	# -----
	# display info to user
	if showInfo :
		print " CNF Infos : \n-----------"
		print " %r variables and %r clauses " % (len(variables), len(clauses))
		print


	# STEP 8 :
	# -----
	# create CNF with empty solutions
	return logic.CNF(clauses,[], heuristic)


