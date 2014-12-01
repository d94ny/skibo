
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

# Implementing Logic in Python

# Input in string :
# a variable is a number
# a literal is a negative or positive number
# One clause per line

# Example:
# -1 2 3
# 1 2 3
# 1 -2 -3
# -1 -2 -3

class Literal:

	# ========= Fields =========== #

	# A literal is a variable or a negation of a variable
	# Here a variable is just a number
	self.polarity
	self.variable
	self.assignment
	self.assigned

	# ====== Constructors ======== #

	# Per default, assignement is None
	def __init__(self, variable, polarity, assignment=None, assigned=False):
		self.polarity = polarity
		self.variable = variable
		self.assignment = assignment
		self.assigned = assigned

	# Deep copy of a literal
	def copy(self):
		return Literal(variable, self.polarity, self.assignment, self.assigned)

	# Equality
	def __eq__(self, other):
        return (self.variable == other.variable)
        	and (self.polarity == other.polarity)

    # Opposite
    def opposite(self,other):
    	return (self.variable == other.variable)
    		and (self.polarity != other.polarity)

	# ======== Methods =========== #	

	# assign a literal
	def assign(self,s):
		self.assignment = s
		self.assigned = True

	# returns the name of the literal for humans
	# - denotes a negative polarity
	def name(self):
		return self.variable if self.polarity else '-' + self.variable

class Clause:

	# ========= Fields =========== #

	# A clause is a disjunction over literals
	# use a set, as duplicate literals are not important
	self.literals = set()

	# ====== Constructors ======== #

	# Clause Constructor
	def __init__(self, literals):
		self.literals = literals

	# Deep copy of a clause
	def copy(self):
		literals = set([ literal.copy() for literal in self.literals ])
		return Clause(literals)

	# ======== Methods =========== #

	# Returns whether the clause is an empty clause
	# required in STEP 2a
	def isEmpty(self):
		return len(self.literals) == 0

	# A unite clause contains only a single unassigned literal
	def isUnitClause(self):

		# Count the number of unassigned literals
		# and remember the last unit
		lastUnit = None
		units = 0

		for l in self.literals:
			if not l.assigned:
				units += 1
				lastUnit = l

		# If a unit clause, return the unit literal
		if units == 1 :
			return unit
		else:
			return False

class CNF:

	# ========= Fields =========== #

	# A CNF is a conjunction of clauses
	self.clauses = set()

	# ====== Constructors ======== #

	# CNF Constructor
	def __init__(self, clauses):
		self.clauses = clauses

	# CNF from String
	def generate(string):
		
		# IDEA :
		# 1 create a variables for each absolute number
		# 2 create a literal for each number using the variable
		# 3 create a clause for each line
		# 4 add all literals in a line to the corresponding clause
		# 5 add all clauses to the final CNF

	# CNF Factory
	# creates a new CNF with additional assignment
	def new(self, literal, value):

		# Copy all clauses
		clauses = set([ clause.copy() for clause in self.clauses])
		new = CNF(clauses)

		# New to get the literal for new CNF,
		# NOT FOR OLD CNF !
		# ...

	# ======== Methods =========== #

	# Assigns a value to a literal
	def 

	# Get the assignment for the current CNF
	# required in STEP 2b
	def assignment(self):
		return { l.name() : l.value() for l in self.getLiterals() }


	# Returns whether the CNF has no more clauses
	# required in STEP 2b
	def isEmpty(self):
		return len(clauses) == 0

	# Returns a set of all literals
	def getLiterals(self):

		# Using for comprehensions
		return set([ l for l in clause.literals for clause in self.clauses ])


	# Simpify accoring to the following rules
	# 1) remove clauses with at least one TRUE
	# 2) delete all literals with assignement of FALSE
	def simplify(self):

		# get all literals evaluating to TRUE and FALSE
		positives = filter(lambda l : l.value(), self.getLiterals())
		negatives = filter(lambda l : l.value() == False, self.getLiterals())

		# Execute rule 1
		self.clauses = filter(
			lamdba c : len(c.literals.intersection(positives)) == 0,
			self.clauses)

		# Execute rule 2
		for clause in self.clause:
			clause.literals = clause.literals.difference(negatives)


	# Unite Propagation
	# required in STEP 1a
	def unitPropagate(self):

		# Iterate until we have no more unit clauses
		while True:

			# Keep track whether we found a unit
			found = False

			for clause in self.clauses:

				unit = clause.isUnitClause()

				# If we have a unit literal,
				# assign it to True
				if unit :
					unit.assign(True)
					found = True

				# Assigning these to true can creates
				# new unit in other clauses

			# break the while loop if we did not find
			# any more unit literals
			if not found : return

	# Says whether a literal is Pure
	# that is it occurs with only one polarity
	def isPure(self, literal):

		# Check that there is no opposite literal
		opp = filter(lambda l : literal.opposite(l), self.getLiterals())
		return len(opp) == 0

	# Pure Clauses can be removed since they have
	# no constraints on other clauses.
	# Just set the pure literals to true
	# required in STEP 1b
	def pureEliminate(self):

		pures = set()

		# Step 1
		# Find all pure literals
		for literal in self.getLiterals():
			if self.isPure(literal):

				# Assign this literal to be True
				literal.assign(True)
				pures.add(literal)

		# Step 2
		# Remove all clauses containing a pure literal
		self.clauses = filter(
			lambda c : len(c.getLiterals().intersection(pures)) == 0,
			self.clauses)

		# No need to simplify here