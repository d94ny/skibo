
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import random
import branching

# Implementing Logic in Python

class Var:

	# ========= Fields =========== #

	identifier = 0
	assignment = None

	# ====== Constructors ======== #

	# By default the variable has no assignment yet
	def __init__(self, identifier):
		self.identifier = identifier

	# ======== Methods =========== #

	# Assign a value to the variable
	def assign(self, s):
		self.assignment = s

	def __repr__(self):
		return str(self.identifier)

class Literal:

	# ========= Fields =========== #

	# A literal is a variable or a negation of a variable
	variable = None
	polarity = True

	# ====== Constructors ======== #

	def __init__(self, var, polarity):
		self.polarity = polarity
		self.variable = var

	# For humans
	def __repr__(self):
		return str(self.variable) if self.polarity else '-' + str(self.variable)

	# ======== Methods =========== #

	# Returns true when other is the opposite literal
	def opposite(self, other):
		return (self.variable == other.variable) and (self.polarity != other.polarity)

	# assign a literal
	def assign(self,s):
		self.variable.assign((not self.polarity) ^ s)

	# unassign, so that we can use the same literal for
	# multiple CNF's
	def unassign(self):
		self.variable.assign(None)

	# get the value of the literal
	# returns None if not assigned
	def value(self):
		return None if self.variable.assignment == None else (not self.polarity) ^ self.variable.assignment

class Clause:

	# ========= Fields =========== #

	# A clause is a disjunction over literals
	literals = []

	# ====== Constructors ======== #

	# Clause Constructor
	def __init__(self, literals):
		self.literals = literals

	# Return a copy of the clause
	# Only shallow copy, keep same literals !
	def copy(self):
		return Clause(self.literals)

	# For humans
	def __repr__(self):
		return str([ l for l in self.literals ])

	# ======== Methods =========== #

	# Returns whether the clause is an empty clause
	# required in STEP 2a
	def isEmpty(self):
		return len(self.literals) == 0

	# Returns the unite literal if it exists
	def unit(self):
		return self.literals[0] if len(self.literals) == 1 else False

class CNF:

	# ========= Fields =========== #

	# A CNF is a conjunction of clauses
	# solutions contains the positive literals (here just strings)
	clauses = []
	solution = []
	heuristic = 0

	# ====== Constructors ======== #

	# CNF Constructor
	def __init__(self, clauses, solution, heuristic):
		self.clauses = clauses
		self.solution = solution
		self.heuristic = heuristic

	# CNF Factory
	# creates a new CNF
	def copy(self):

		# Copy all clauses
		clauses = [ clause.copy() for clause in self.clauses ]

		# Return a new CNF
		return CNF(clauses, list(self.solution), self.heuristic)

	# For humans
	def __repr__(self):
		return str([ clause for clause in self.clauses])

	# ======== Methods =========== #

	# Returns whether the CNF has no more clauses
	# required in STEP 2b
	# OK FOR 2.0
	def isEmpty(self):
		return len(self.clauses) == 0

	# Returns whether the CNF contains an empty clause
	# OK FOR 2.0
	def emptyClause(self):

		for clause in self.clauses:
			if len(clause.literals) == 0:
				return True
		return False

	# Returns a list of all literals
	def getLiterals(self):
		return [ l for clause in self.clauses for l in clause.literals ]

	# Branch Split
	def branch(self):

		# branching
		return branching.heuristics[self.heuristic](self)


	# Returns solution
	def solutions(self):

		# Sort the solution by absolute value
		return sorted(self.solution,
			key=lambda x: abs(int(x)))

	# Simpify CNF
	def simplify(self):

		# remove clauses with at least one TRUE
		self.clauses = filter(
			lambda c : len(filter(lambda l : l.value(), c.literals)) == 0,
			self.clauses)

		# delete all literals with assignement of FALSE
		for clause in self.clauses:
			clause.literals = filter( lambda l : l.value() != False, clause.literals)

	# Assigns a value to a literal and simplifies the CNF direcrtly afterwards
	def assign(self, literal, value):

		# 1. Save the assignement in the solutions
		if value:
			self.solution.append(str(literal))

		# 2. Simplify the CNF
		literal.assign(value)
		self.simplify()
		literal.unassign()

	# Unite Propagation
	# required in STEP 1a
	def unitPropagate(self):

		# Iterate until we have no more unit clauses
		while True:

			# Keep track whether we found a unit
			found = False

			for clause in self.clauses:

				unit = clause.unit()

				# If we have a unit literal,
				# assign it to True
				if unit :

					self.assign(unit, True)
					found = True

				# Assigning these to true can creates
				# new unit in other clauses

			# break the while loop if we did not find
			# any more unit literals or we have an empty clause
			if self.emptyClause() or not found : return

	# Says whether a literal is Pure
	# that is it occurs with only one polarity in the cnf
	def isPure(self, literal):

		for l in self.getLiterals():
			if  literal.opposite(l) : return False

		return True


	# Pure Clauses can be removed
	# Just set the pure literals to true
	# required in STEP 1b
	# Unfortunately this is really slow
	def pureEliminate(self):

		for literal in self.getLiterals():
			if self.isPure(literal):

				# Assign this literal to be True
				self.assign(literal, True)



