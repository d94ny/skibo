
# 15-354
# Computational Discrete Math
# -------------------
# Simple SAT Solver
# -------------------
# Daniel Ballle 2014

import random

# First literal
def firstLiteral(cnf):
	return cnf.getLiterals()[0]
	
# Random Heuristic
def randomLiteral(cnf):
	return random.choice(cnf.getLiterals())


# Global variable with all heuristics
heuristics = [firstLiteral, randomLiteral]

