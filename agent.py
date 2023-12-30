import reward
from knownledgeBase import *
from dpll import *
from collections import deque

R = [-1, 0, 1, 0]
C = [0, -1, 0, 1]

def escape(self):
    self.__isEscaping = True

def isEscaping(self):
    return self.__isEscaping


def nearestSafeCell(self, n): #return coordinate
    vst = set()
    q = deque()
    q.append(self.__agentLoc)
    result = []

    while len(result) == 0:
        r = q[0][0]
        c = q[0][1]
        q.popleft()
        vst.add([r, c])

        for k in range(0, 4):
            newR = r + R[k]
            newC = c + C[k]

            if newR < 0 or n < newR or newC < 0 or n < newC:
                continue
            
            newCell = str(newR) + '_' + str(newC)
            if newCell in self.__safe:
                result = [newR, newC]
                self.__visited.append(newCell)
                self.__safe.remove(newCell)
                break
            elif newCell in self.__visited and [newR, newC] not in vst:
                vst.add([newR, newC])
                q.append([newR, newC])
    
    return result


def findASafeStep(self, mapSize): #return coordinate
    #update safe list
    result, groundTruth = unitPropagation(self.__kb.__clauses)
    for cell in self.__unknown:
        p = 'P' + cell
        w = 'W' + cell
        if groundTruth[p] != None and groundTruth[w] != None:
            self.__unknown.remove(cell)
            if not groundTruth[p] and not groundTruth[w]:
                self.__safe.append(cell)

    return nearestSafeCell(self, mapSize)


class Agent:
    def __init__(self):
        self.__kb = KnownledgeBase()
        self.__agentLoc = []    #location,                  format: [row, col]
        self.__unknown = []     #frontier cells, unknown,   format: 'row_col'
        self.__safe = []        #frontier cells, safe,      format: 'row_col'
        self.__visited = []     #visited cells,             format: 'row_col'
        self.__foundExit = False
        self.__isAlive = True
        self.__point = 0
        self.__isEscaping = False

    def __str__(self):
        pass

    escape = escape
    isEscaping = isEscaping

    def updateKB(self):
        pass

    def forceAStep(self):
        pass

    findASafeStep = findASafeStep
    nearestSafeCell = nearestSafeCell

    def updateInfo(self, map):
        pass

    def playPath(self, des):
        pass

    def shoot(self):
        pass

    @property
    def kb(self):
        return self.__kb

    @kb.setter
    def kb(self, kb: list):
        self.__kb = kb

    @property
    def agentLoc(self):
        return self.__agentLoc

    @agentLoc.setter
    def agentLoc(self, agentLoc: list):
        self.__agentLoc = agentLoc

    @property
    def safe(self):
        return self.__safe

    @safe.setter
    def safe(self, safe: list):
        self.__safe = safe

    @property
    def visited(self):
        return self.__visited

    @visited.setter
    def visited(self, visited: list):
        self.__visited = visited

    @property
    def foundExit(self):
        return self.__foundExit

    @foundExit.setter
    def foundExit(self, foundExit: bool):
        self.__foundExit = foundExit

    @property
    def isAlive(self):
        return self.__isAlive

    @isAlive.setter
    def isAlive(self, isAlive: bool):
        self.__isAlive = isAlive

    @property
    def point(self):
        return self.__point
    
    @point.setter
    def point(self, point):
        self.__point = point
