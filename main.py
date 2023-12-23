from functions import *

if __name__ == '__main__':
    map, agentCoord = input('tests/test1.txt')
    kb = []
    dead = False
    escape = False
    foundExit = False
    agent =

    while not dead and not escape:
        agent.updateInfo(map)
        nextRoom = []
        if not foundExit:
            nextRoom = agent.forceAStep()
        else:
            nextRoom = agent.findASafeStep()
            if nextRoom == [-1, -1]:
                nextRoom = [1, 1]
                escape = True
        
        agent.playPath(map)



    
