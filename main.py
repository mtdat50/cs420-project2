from functions import *
from agent import Agent
from map import Map


def main():
    agent = Agent()
    map, agent.agentLoc = input("tests/test1.txt")

    while agent.isAlive and agent.escape():
        agent.updateInfo(map)
        nextRoom = []
        if agent.foundExit:
            nextRoom = agent.forceAStep()
        else:
            nextRoom = agent.findASafeStep(map.size())
            if nextRoom == [-1, -1]:
                nextRoom = [1, 1]
                escape = True

        agent.playPath(nextRoom)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()
