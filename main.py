
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import sys
import solver
import convert

# Get the file and heuristic from paramters

# Verify that a file was provided
if len(sys.argv) < 2:

	print "Please provide a CNF file"
	exit(0)


# Determine the heuristic
if len(sys.argv) < 3 :

	print "No branching heuristic was specified."
	heuristic = 0

else :
	# TODO Verify it's under X
	heuristic = int(sys.argv[2])


# FILES EXAMPLES:
# aim-50-1_6-yes1-4.cnf.txt (true) YES
# aim-100-1_6-no-1.cnf.txt (false)
# bf0432-007.cnf.txt (?)
# dubois20.cnf.txt (false)
# dubois21.cnf.txt (false)
# dubois22.cnf.txt (false)
# factoring2.txt (HARD)
# hole6.cnf.txt (false) WORKS
# simple_v3_c2.cnf.txt


# get file
file = sys.argv[1]

f = open('../lab/'+file)
string = f.read()

# Convert the file to Logic
cnf = convert.generate(string, heuristic)

print "Solving %r ... " % (file)
print solver.solve(cnf)