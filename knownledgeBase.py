from dpll import *


def solve(self, assignment, allowBranching = False):
    if allowBranching:
        result, assignment = dpll(self.clauses)
    else:
        result, assignment = unitPropagation(self.clauses, {})
    return assignment

def addClause(self, clause):
    self.clauses.append(clause)
    for literal in clause:
        var = literal.replace('-', '')
        if var not in self.vars:
            self.vars.append(var)

class KnownledgeBase:
    def __init__(self):
        self.__clauses = []
        self.__vars = []

    solve = solve
    addClause = addClause

    @property
    def clauses(self):
        return self.__clauses

    @property
    def vars(self):
        return self.__vars