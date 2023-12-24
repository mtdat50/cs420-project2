import reward

class Agent:
    def __init__(self):
        self.__kb = []
        self.__agentLoc = []
        self.__safe = []
        self.__visited = []
        self.__foundExit = False
        self.__isAlive = True
        self.__point = 0

    def __str__(self):
        pass

    def escape(self):
        pass

    def updateKB(self):
        pass

    def inferenceKB(self):
        pass

    def forceAStep(self):
        pass

    def findASafeStep(self):
        pass

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
