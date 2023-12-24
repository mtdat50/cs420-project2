from functions import *
from agent import Agent


def main():
    map, agentCoord = input("tests/test1.txt")
    agent = Agent()

    while agent.isAlive and agent.escape():
        agent.updateInfo(map)
        nextRoom = []
        if agent.foundExit:
            nextRoom = agent.forceAStep()
        else:
            nextRoom = agent.findASafeStep()
            if nextRoom == [-1, -1]:
                nextRoom = [1, 1]
                escape = True

        agent.playPath(nextRoom)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()
