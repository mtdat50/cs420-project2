from functions import *
from agent import Agent
from map import Map


def main():
    agent = Agent()
    map, agent.agentLoc = input("tests/test1.txt")

    # agent.foundExit = True
    while agent.isAlive and not agent.isEscaping:
        print('===========================', agent.agentLoc)
        agent.perceiveEnvironment(map)
        print(agent.kb.clauses)

        nextRoom = []
        if agent.foundExit:
            nextRoom = agent.findASafeStep(map.size())
            if nextRoom == [-1, -1]:
                nextRoom = [1, 1]
                agent.isEscaping = True
                print('escapse')
                
        # else:
        #     nextRoom = agent.forceAStep()

        agent.playPath(nextRoom)
        agent.agentLoc = nextRoom

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()
