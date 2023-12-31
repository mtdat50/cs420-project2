from functions import *
from agent import Agent
from map import Map
import pygame
from constants import *
import sys
from Cell import Cell
from constants import CELL_SIZE
import random


def main():
    agent = Agent()
    map, agent.agentLoc = input("tests/test1.txt")

    # agent.foundExit = True
    while agent.isAlive and not agent.isEscaping:
        print('===========================', agent.agentLoc)
        agent.perceiveEnvironment(map)
        print('kb: ', agent.kb.clauses)

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

    # General initializations
    pygame.display.set_caption('Wumpus World')
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("freesansbold" , 18 , bold = True)

    # Game screen
    screen_width = map.size() * CELL_SIZE
    screen_height = map.size() * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.HWSURFACE)

    # Cell Group
    cellGroup = pygame.sprite.Group()
    for i in range(map.size()):
        for j in range(map.size()):
            new_cell = Cell("Graphics\\catacombs_", CELL_SIZE/2 + CELL_SIZE * j, CELL_SIZE/2 + CELL_SIZE * i)
            cellGroup.add(new_cell)


    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        cellGroup.draw(screen)
        cellGroup.update()

        clock.tick(120)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()