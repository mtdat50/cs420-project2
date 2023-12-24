from dpll import *

class KnownledgeBase:
    def __init__(self):
        self.__kb = []
        self.__vars = []

    def solve(self, assignment, allowBranching = False):
        result, assignment = 0, 0
        if allowBranching:
            result, assignment = dpll(self.__kb, assignment)
        else:
            result, assignment = unitPropagation(self.__kb, assignment)
        return assignment
    
    def add(self, clause):
        self.__kb.append(clause)
        for var in clause:
            if var not in self.__vars:
                self.__vars.append(var)
