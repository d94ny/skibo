
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


# STEP 1 :
# -----
# Verify that a CNF file was given
if len(sys.argv) < 2:

	print "ERROR: Please provide a CNF file"
	exit(0)


# STEP 2 :
# -----
# Retrieve all optional arguments
try:
	optlist, args = getopt.getopt(sys.argv[2:], '', ['heuristic=','comments','info','help','pure'])

except getopt.GetoptError as err:
	# Display the error
	print str(err)
	exit(0)


# STEP 3 :
# -----
# Handle the optional arguments

# Set default values for all options
heuristic, comments, info, _help, pure = "firstLiteral", False, False, False, False

# Iterate over optional arguments
for option, value in optlist:
	if option == "--heuristic":
		heuristic = value
	elif option == "--comments":
		comments = True
	elif option == "--info":
		info = True
	elif option == "--help":
		_help = True
	elif pure == "--pure":
		pure = True

# Display help is needed
if _help:
	print "Usage : main.py CNF [--heuristic=...] [--comments] [--info] [--help] [--pure]"
	exit(0)


# STEP 4 :
# -----
# Open the CNF file
file = sys.argv[1]
f = open('../lab/'+file)
string = f.read()

# Clear terminal 
print chr(27) + "[2J"
print "Solving %s using heuristic %s... \n\n" % (file, heuristic)


# STEP 5 :
# -----
# Convert the file to a CNF
try:
	# Generate CNF from string with heuristic
	# Also takes comments and info
	cnf = convert.generate(string, heuristic, info, comments)
except:
	print "ERROR : The CNF file seems to be invalid"
	exit(0)

# Keep track of failures
failures = [0]


# STEP 6 :
# -----
# Solve the CNF and mesure performance
start = time.time()
sat = solver.solve(cnf, pure, failures)
end = time.time()


# STEP 7 :
# -----
# Display results

# If CNF is satisfiable, solver will print a message
# Otherwise notify user of failure
if not sat :
	print " Solution : \n-----------"
	print " unsatisfiable !"

# If info display number of failed splits
if info :
	print " Failed splits : %r " % failures[0]

# Print for better display
print

# Finally display performance
if info:
	print " Performance : \n-----------"
	print " Solved in %r seconds." % (round(end - start, 4))
	print


