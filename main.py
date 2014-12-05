
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Balle 2014

# 
# Main file responsible for reading a CNF formatted file
# and setting command arguments
#

import sys
import solver
import convert
import time
import getopt
import branching


# STEP 1 :
# -----
# Verify that a CNF file was given
if len(sys.argv) < 2:

	print "ERROR : Please provide a CNF file"
	exit(0)


# STEP 2 :
# -----
# Retrieve all optional arguments
try:
	optlist, args = getopt.getopt(sys.argv[2:], '', ['heuristic=','comments','info','help','pure', 'unit'])

except getopt.GetoptError as err:
	# Display the error
	print str(err)
	exit(0)


# STEP 3 :
# -----
# Handle the optional arguments

# Set default values for all options
heuristic, comments, info, _help, pure, unit = "firstLiteral", False, False, False, False, False

# Iterate over optional arguments
for option, value in optlist:
	if option == "--heuristic":
		heuristic = value

		# Also set constants for some heuristics
		if value == "momsf":

			inp = 0
			while inp == 0:
				inp = int(raw_input("Please set a positive value for k : "))

			branching.setK(inp)

	elif option == "--comments":
		comments = True
	elif option == "--info":
		info = True
	elif option == "--help":
		_help = True
	elif option == "--pure":
		pure = True
	elif option == "--unit":
		unit = True

# Display help is needed
if _help:
	print "Usage : main.py CNF [--heuristic=...] [--pure] [--unit] [--comments] [--info] [--help]"
	exit(0)


# STEP 4 :
# -----
# Open the CNF file
file = sys.argv[1]
try:
	f = open(file)
	string = f.read()
except Exception as err:
	# Display the error
	print "ERROR : Could not read CNF file"
	exit(0)

# Clear terminal 
print chr(27) + "[2J"
print "Solving %s using heuristic %s ... \n\n" % (file, heuristic)


# STEP 5 :
# -----
# Convert the file to a CNF
try:
	# Generate CNF from string with heuristic
	# Also takes comments and info
	cnf = convert.generate(string, heuristic, info, comments)
except Exception as err:
	print "ERROR : The CNF file seems to be invalid"
	print err
	exit(0)

# Also verify that the cnf does not already have an empty clause
if cnf.emptyClause():
	print "ERROR : The CNF has already an empty clause"
	exit(0)

# Keep track of total splits and failed splits
splits = [0,0]


# STEP 6 :
# -----
# Solve the CNF and mesure performance
start = time.time()
sat = solver.solve(cnf, pure, unit, splits)
end = time.time()

# STEP 7 :
# -----
# Display results

if sat :
	# Print the solution
	print " Solution : \n-----------"
	print " satisfiable !"
	print " positive literals : (%d) " % len(sat.solutions())
	print " " + ', '.join(sat.solutions())
	print

else :
	print " Solution : \n-----------"
	print " unsatisfiable !"
	print

# If info display number of failed splits
if info :
	print " Stats : \n-----------"
	print " Used heuristic : %r " % heuristic
	print " Failed splits : %r " % splits[1]
	print " Successful splits : %r " % (splits[0] - splits[1])

	# If it was satisfiable
	if sat:
		print " Number of units propagated : %r " % (len(sat.units))
		print " Number of pure eliminations : %r " % (len(sat.pures))
	
	print

# Finally display performance
if info:
	print " Performance : \n-----------"
	print " Solved in %r seconds." % (round(end - start, 4))
	print


