import reward
from knownledgeBase import *
from dpll import *
from collections import deque

R = [-1, 0, 1, 0]
C = [0, -1, 0, 1]

def forceAStep(self, n): #return coordinate, isShooting, maybePit 
    result, groundTruth = unitPropagation(self.kb.clauses, {})

    vst = set()
    q = deque()
    q.append(self.agentLoc)
    result = [-1, -1]
    shooting = False
    maybePit = True

    while len(q) != 0:
        r = q[0][0]
        c = q[0][1]
        q.popleft()
        vst.add((r, c))
        if (r, c) == (2, 1):
            i = 0

        for k in range(0, 4):
            newR = r + R[k]
            newC = c + C[k]

            if min(newR, newC) < 1 or n < max(newR, newC) \
                or (newR, newC) in vst:
                continue
            
            newCell = str(newR) + '_' + str(newC)
            p = 'P' + newCell
            w = 'W' + newCell
            if newCell not in self.visited \
                and (newCell in self.unknown or not groundTruth.get(p)):
                if groundTruth.get(p) == False: # not pit, could be wumpus
                    result = [newR, newC]
                    shooting = True
                    maybePit = False
                    q.clear() # found a room that is not pit
                    break
                elif groundTruth.get(p) == None and result == [-1, -1]: # could be pit
                    result = [newR, newC]
                    if groundTruth.get(w) != False:
                        shooting = True
            elif newCell in self.visited:
                vst.add((newR, newC))
                q.append([newR, newC])
    
    return result, shooting, maybePit


def nearestSafeCell(self, n): #return coordinate
    if (self.agentLoc[0], self.agentLoc[1]) == (3, 1):
        iodjhgisdg = 0
    vst = set()
    q = deque()
    q.append(self.agentLoc)
    result = [-1, -1]

    while len(q) != 0:
        r = q[0][0]
        c = q[0][1]
        q.popleft()
        vst.add((r, c))

        for k in range(0, 4):
            newR = r + R[k]
            newC = c + C[k]

            if min(newR, newC) < 1 or n < max(newR, newC):
                continue
            
            newCell = str(newR) + '_' + str(newC)
            if newCell in self.safe:
                result = [newR, newC]
                q.clear() #found nearest safe room
                break
            elif newCell in self.visited and (newR, newC) not in vst:
                vst.add((newR, newC))
                q.append([newR, newC])
    
    return result


def findASafeStep(self, mapSize): #return coordinate
    #update safe list
    # print(self.kb.clauses)
    result, groundTruth = unitPropagation(self.kb.clauses, {})
    # print(result, groundTruth)
    copyOfUnknown = self.unknown.copy()
    for cell in copyOfUnknown:
        p = 'P' + cell
        w = 'W' + cell
        if groundTruth.get(p) != None and groundTruth.get(w) != None:
            self.unknown.remove(cell)
            if not groundTruth[p] and not groundTruth[w]:
                if cell not in self.safe:
                    self.safe.append(cell)

    return nearestSafeCell(self, mapSize)


def perceiveEnvironment(self, map):
    # visited
    currentCell = str(self.agentLoc[0]) + '_' + str(self.agentLoc[1])
    print('map :', map[self.agentLoc[0]][self.agentLoc[1]])
    if currentCell in self.visited:
        return
    self.visited.append(currentCell)
    if currentCell in self.safe:
        self.safe.remove(currentCell)
    
    if currentCell == '1_1':
        self.foundExit = True
    
    # gold
    if 'G' in map[self.agentLoc[0]][self.agentLoc[1]]:
        self.point += reward.REWARD_FOR_GRABBING_GOLD
    if 'B' in map[self.agentLoc[0]][self.agentLoc[1]] or\
        'S' in map[self.agentLoc[0]][self.agentLoc[1]]:
        self.point += reward.PUNISHMENT_FOR_DYING

    surroundingCells = []
    for k in range(0, 4):
        newR = self.agentLoc[0] + R[k]
        newC = self.agentLoc[1] + C[k]
        newCell = str(newR) + '_' + str(newC)
        if min(newR, newC) < 1 or map.size() < max(newR, newC):
            continue
        if newCell not in self.unknown and \
            newCell not in self.safe and \
            newCell not in self.visited:
            self.unknown.append(newCell)
        surroundingCells.append(newCell)

    # breeze
    if 'B' in map[self.agentLoc[0]][self.agentLoc[1]]:
        PClause = [('P' + cell) for cell in surroundingCells]
        self.kb.addClause(PClause, '0_0')
    else:
        for cell in surroundingCells:
            self.kb.addClause(['-P' + cell], '0_0')

    # stench
    if 'S' in map[self.agentLoc[0]][self.agentLoc[1]]:
        PClause = [('W' + cell) for cell in surroundingCells]
        self.kb.addClause(PClause, currentCell)
    else:
        self.kb.remove(currentCell)
        for cell in surroundingCells:
            self.kb.addClause(['-W' + cell], currentCell)


def shoot(self, target, map):
    self.point += reward.PUNISHMENT_FOR_SHOOTING
    if 'W' not in map[target[0]][target[1]]: # no wumpus killed
        return
    
    print(map._Map__map[target[0]][target[1]])
    map[target[0]][target[1]] = map[target[0]][target[1]].replace('W', '')
    print(map._Map__map[target[0]][target[1]])
    for r in range(1, map.size() + 1):
        for c in range(1, map.size() + 1):
            map[r][c] = map[r][c].replace('S', '')
            map[r][c] = map[r][c].replace('B', '')
    map.updateInfo()

    if 'S' not in map[self.agentLoc[0]][self.agentLoc[1]]: # if stench disappear
        currentCell = str(self.agentLoc[0]) + '_' + str(self.agentLoc[1])
        self.kb.remove(currentCell)
    
    for k in range(4):
        newR = target[0] + R[k]
        newC = target[1] + C[k]

        if min(newR, newC) < 1 or map.size() < max(newR, newC) or \
            (newR, newC) == (self.agentLoc[0], self.agentLoc[1]):
            continue
        newCell = str(newR) + '_' + str(newC)
        if newCell in self.visited:
            self.visited.remove(newCell)
            if newCell not in self.safe:
                self.safe.append(newCell)


def playPath(self, des):
    q = deque()
    q.append(self.agentLoc)
    trace = {}
    trace[(self.agentLoc[0], self.agentLoc[1])] = (0, 0)

    while len(q) != 0:
        r = q[0][0]
        c = q[0][1]
        q.popleft()

        for k in range(0, 4):
            newR = r + R[k]
            newC = c + C[k]
            newCell = str(newR) + '_' + str(newC)
            
            if (newR, newC) == (des[0], des[1]): #found path
                trace[(des[0], des[1])] = (r, c)
                q.clear() 
                break
            elif newCell in self.visited and trace.get((newR, newC)) == None:
                trace[(newR, newC)] = (r, c)
                q.append([newR, newC])

    # tracing path
    r = des[0]
    c = des[1]
    result = []
    while (r, c) != (self.agentLoc[0], self.agentLoc[1]):
        result.append([r, c])
        prevCell = trace[(r, c)]
        r = prevCell[0]
        c = prevCell[1]
    result.reverse()
    return result


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

    perceiveEnvironment = perceiveEnvironment

    forceAStep = forceAStep

    findASafeStep = findASafeStep
    nearestSafeCell = nearestSafeCell

    playPath = playPath

    shoot = shoot

    @property
    def kb(self):
        return self.__kb

    @property
    def agentLoc(self):
        return self.__agentLoc

    @agentLoc.setter
    def agentLoc(self, agentLoc: list):
        self.__agentLoc = agentLoc

    @property
    def unknown(self):
        return self.__unknown

    @property
    def safe(self):
        return self.__safe

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

    @property
    def isEscaping(self):
        return self.__isEscaping
    
    @isEscaping.setter
    def isEscaping(self, isEscaping: bool):
        self.__isEscaping = isEscaping
