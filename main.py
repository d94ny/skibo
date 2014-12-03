
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import sys
import solver
import convert
import time
import getopt

# List of arguments
# <cnf> : cnf file
# --comments : show file comments
# --info : show full info (number of clauses/variables, number of fails, performance)
# --help : display help page
# --heuristic <heuristic> : select heuristic to use
# -k : specify the constant k for MOMSF


# STEP 1 : Verify that a CNF file was given
if len(sys.argv) < 2:

	print "ERROR: Please provide a CNF file"
	exit(0)

# STEP 2 : Retrieve all optional arguments
try:
	optlist, args = getopt.getopt(sys.argv[2:], '', ['heuristic=','comments','info','help'])

except getopt.GetoptError as err:
	# Display the error
	print str(err)
	exit(0)

# STEP 3 : Handle the optional arguments

# Set default values for all options
heuristic, comments, info, _help = "firstLiteral", False, False, False

# Iterate over optional arguments
for option, value in optlist:
	if option == "--heuristic":
		heuristic = value
	elif option == "--comments":
		comments = True
	elif option == "--info":
		info = True

# Display help is needed
if _help:
	print "Usage : main.py CNF [--heuristic=...] [--comments] [--info] [--help]"
	exit(0)

# FILES EXAMPLES:
# aim-50-1_6-yes1-4.cnf.txt (true) WORK VERY WELL
# aim-100-1_6-no-1.cnf.txt (false)
# bf0432-007.cnf.txt (?)
# dubois20.cnf.txt (false)
# dubois21.cnf.txt (false)
# dubois22.cnf.txt (false)
# factoring2.txt (HARD)
# hole6.cnf.txt (false) WORKS WELL !!
# simple_v3_c2.cnf.txt


# STEP 4 : Get the CNF file
file = sys.argv[1]
f = open('../lab/'+file)
string = f.read()

# Clear terminal 
print chr(27) + "[2J"
print "Solving %s using heuristic %s... \n\n" % (file, heuristic)

# STEP 5 : Convert the file to a CNF
try:
	# Generate CNF from string with heuristic
	# Also takes comments and info
	cnf = convert.generate(string, heuristic, info, comments)
except:
	print "ERROR : The CNF file seems to be invalid"
	exit(0)


start = time.time()
print solver.solve(cnf)
end = time.time()

if info:
	print " Performance : \n-----------"
	print " Solved in %r seconds." % (end - start)
	print


