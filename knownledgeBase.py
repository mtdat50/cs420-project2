from dpll import *


def solve(self, assignment, allowBranching = False):
    if allowBranching:
        result, assignment = dpll(self.__clauses)
    else:
        result, assignment = unitPropagation(self.__clauses)
    return assignment

def addClause(self, clause):
    self.__clauses.append(clause)
    for literal in clause:
        var = literal.replace('-', '')
        if var not in self.__vars:
            self.__vars.append(var)

class KnownledgeBase:
    def __init__(self):
        self.__clauses = []
        self.__vars = []

    solve = solve
    addClause = addClause
