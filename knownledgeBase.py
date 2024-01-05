from dpll import *


def solve(self, assignment, allowBranching = False):
    if allowBranching:
        result, assignment = dpll(self.clauses)
    else:
        result, assignment = unitPropagation(self.clauses, {})
    return assignment

def addClause(self, clause, source):
    self.sources.append(source)
    self.clauses.append(clause)

def remove(self, source):
    for i, s in enumerate(self.sources):
        if s == source:
            self.sources.pop(i)
            self.clauses.pop(i)
            break

class KnownledgeBase:
    def __init__(self):
        self.__clauses = []
        self.__sources = []

    solve = solve
    addClause = addClause
    remove = remove

    @property
    def clauses(self):
        return self.__clauses
    
    @property
    def sources(self):
        return self.__sources