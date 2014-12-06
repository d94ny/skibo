
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Balle 2014

#
# Implements logical components necessary for
# the SAT solver
#

import random
import branching


# Var represents a variable
#
# @field identifier : an unique integer ID
# @field assignment : an assignment (True, False or None)
#
class Var:

	# ========= Fields =========== #

	identifier = 0
	assignment = None

	# ====== Constructors ======== #

	# Variable Constructor
	# Takes no assignment per default
	def __init__(self, identifier):
		self.identifier = identifier


	# Equality
	# Two variables are equal if their ID's are
	def __eq__(self,other):
		return self.identifier == other.identifier

	# Hash for Dictionaries
	def __hash__(self):
		return hash(self.identifier)

	# ======== Methods =========== #

	# Assign a value to the variable
	def assign(self, s):
		self.assignment = s


	# Representation for humans
	def __repr__(self):
		return str(self.identifier)



# Literal represents a literal 
# i.e a variable or its negation
#
# @field variable : the underlying variable
# @field polarity : the polarity of the variable
#                   False if variable is negated
#
class Literal:

	# ========= Fields =========== #

	variable = None
	polarity = True

	# ====== Constructors ======== #

	# Constructor takes both a variable and a polarity
	def __init__(self, var, polarity):
		self.polarity = polarity
		self.variable = var


	# Representation for humans
	def __repr__(self):
		return str(self.variable) if self.polarity else '-' + str(self.variable)


	# Hash for Dictionaries
	def __hash__(self):
		return hash(self.polarity) + hash(self.variable)

	# ======== Methods =========== #


	# Returns true when other is the opposite literal
	def opposite(self, other):
		return (self.variable == other.variable) and (self.polarity != other.polarity)


	# Assigns a value to a literal
	# We assign the corresponding variable depending
	# on the polarity of the literal
	def assign(self,s):
		self.variable.assign((not self.polarity) ^ s)


	# Unassigns a literal, so that we can use the
	# same literal for multiple CNF's
	def unassign(self):
		self.variable.assign(None)


	# Get the value of the literal
	# Returns None if not assigned
	def value(self):
		return None if self.variable.assignment == None else (not self.polarity) ^ self.variable.assignment



# A Clause is disjunction over literals
#
# @field literals : a list of literals
#
class Clause:

	# ========= Fields =========== #

	literals = []

	# ====== Constructors ======== #

	# Clause Constructor
	def __init__(self, literals):
		self.literals = literals


	# Return a copy of the clause
	# Only shallow copy, keep same literals
	def copy(self):
		return Clause(self.literals)


	# Representation for humans
	def __repr__(self):
		return str([ l for l in self.literals ])

	# ======== Methods =========== #


	# Returns whether the clause is an empty clause
	# required in STEP 2a of solver.py
	def isEmpty(self):
		return len(self.literals) == 0


	# Returns the unite literal if it exists
	# (a unite literal is the only unassigned literal in a clause)
	# Otherwise returns False
	def unit(self):
		return self.literals[0] if len(self.literals) == 1 else False



# A CNF is a conjunction of clauses
#
# @field clauses : list of clauses
# @field solution : keeps track of positively assigned literals
# @field heuristic : the name of the heuristic used for the
#                    branching step
# @field units : contains literals determined by unitPropagation
# @field pures : contains literals determined by pureElimination
#
class CNF:

	# ========= Fields =========== #

	clauses = []
	solution = []
	heuristic = ""
	units = []
	pures = []

	# ====== Constructors ======== #


	# CNF Constructor
	def __init__(self, clauses, solution, heuristic, units, pures):
		self.clauses = clauses
		self.solution = solution
		self.heuristic = heuristic
		self.units = units
		self.pures = pures


	# CNF Factory : creates a new CNF
	def copy(self):

		# Copy all clauses
		clauses = [ clause.copy() for clause in self.clauses ]

		# Return a new CNF
		return CNF(clauses, list(self.solution), self.heuristic, list(self.units), list(self.pures))


	# Representation for humans
	def __repr__(self):
		return str([ clause for clause in self.clauses])

	# ======== Methods =========== #

	# Returns whether the CNF has no more clauses
	# required in STEP 2b
	def isEmpty(self):
		return len(self.clauses) == 0


	# Returns whether the CNF contains an empty clause
	# required in STEP 2a
	def emptyClause(self):

		for clause in self.clauses:
			if len(clause.literals) == 0:
				return True
		return False


	# Returns a list of all literals in this CNF
	def getLiterals(self):
		return [ l for clause in self.clauses for l in clause.literals ]


	# Branch Split : selects a unassigned literal
	# according to the heuristic
	def branch(self):

		# Branching heuristics is a dictionary (Map)
		# of available heuristics
		try:
			return branching.heuristics[self.heuristic](self)
		except Exception as err:
			print "ERROR : The heuristic %s does not exist" % (self.heuristic)
			print err
			exit(0)


	# Returns the solution
	# a list of positively assigned literals
	def solutions(self):

		# Sort the solution by absolute value
		return sorted(self.solution,
			key=lambda x: abs(int(x)))


	# Simplify CNF using the assignment of literals
	# according to the following rules
	def simplify(self):

		# RULE 1 : remove clauses with at least one TRUE
		self.clauses = filter(
			lambda c : len(filter(lambda l : l.value(), c.literals)) == 0,
			self.clauses)

		# RULE 2 : delete all literals with assignment of FALSE
		for clause in self.clauses:
			clause.literals = filter( lambda l : l.value() != False, clause.literals)


	# Assigns a value to a literal
	# and simplifies the CNF directly afterwards
	def assign(self, literal, value):

		# 1. Save the assignment in the solutions
		if value:
			self.solution.append(str(literal))

		# 2. Simplify the CNF
		literal.assign(value)
		self.simplify()
		literal.unassign()

		# Assignments are here only used to
		# simplify the CNF in a simple manner


	# Unite Propagation
	# Removes all unit clauses (clauses with one literal)
	# required in STEP 1a
	def unitPropagate(self):

		# Iterate until we have no more unit clauses
		while True:

			# Keep track whether we found a unit
			found = False

			for clause in self.clauses:

				# Returns the unit if it exists otherwise False
				unit = clause.unit()

				# If we have a unit literal,
				# assign it to True (this removes the corresponding clause)
				if unit :

					self.units.append(str(unit))
					self.assign(unit, True)
					found = True

			# break the while loop if we did not find
			# any more unit literals or we have an empty clause
			if self.emptyClause() or not found : return


	# Returns whether a literal is Pure
	# that is it occurs with only one polarity in the cnf
	def isPure(self, literal):

		for l in self.getLiterals():
			if literal.opposite(l) :
				return False

		return True


	# Pure Elimination : Pure Clauses can be removed
	# Just set the pure literals to true
	# required in STEP 1b
	def pureEliminate(self):

		# Force re-computation of literals
		# until no more found

		found = True
		while found:

			found = False

			# Remove duplicates
			for literal in set(self.getLiterals()):

				if self.isPure(literal):

					# Assign this literal to be true
					self.assign(literal, True)
					self.pures.append(str(literal))
					found = True

					break


