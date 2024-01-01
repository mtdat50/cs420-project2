from zmq import proxy
from functions import *
from agent import Agent
from map import Map
from constants import *
import sys
import pygame
from Cell import Cell
from Player import Player
from Object import Object
from constants import CELL_SIZE

def getCellIDinGroup(pos_x: int, pos_y: int, map_size: int):
    return pos_x * map_size + pos_y

def main():
    agent = Agent()
    map, agent.agentLoc = input("tests/test1.txt")

    loop_n = map.size() + 1 # true loop size, not map's size

    # agent.foundExit = True
    # while agent.isAlive and not agent.isEscaping:
    #     print('===========================', agent.agentLoc)
    #     agent.perceiveEnvironment(map)
    #     print('kb: ', agent.kb.clauses)

    #     nextRoom = []
    #     if agent.foundExit:
    #         nextRoom = agent.findASafeStep(map.size())
    #         if nextRoom == [-1, -1]:
    #             nextRoom = [1, 1]
    #             agent.isEscaping = True
    #             print('escapse')
    #     # else:
    #     #     nextRoom = agent.forceAStep()

    #     agent.playPath(nextRoom)
    #     agent.agentLoc = nextRoom

    # General initializations
    pygame.display.set_caption('Wumpus World')
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("freesansbold" , 18 , bold = True)

    # Game screen
    screen_width = loop_n * CELL_SIZE
    screen_height = loop_n * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.HWSURFACE)

    # Pits Group
    pitGroups = pygame.sprite.Group()

    # Monster Group
    monsterGroups = pygame.sprite.Group()

    # Cell Group
    cellGroup = pygame.sprite.Group()
    for i in range(loop_n):
        for j in range(loop_n):
            new_cell = Cell("Graphics\\catacombs_", CELL_SIZE/2 + CELL_SIZE * j, CELL_SIZE/2 + CELL_SIZE * i)
            cellGroup.add(new_cell)
            
            if 'P' in map[i][j]:
                newPitGroup = pygame.sprite.Group()
                pit = Object("Graphics\\shaft.png", new_cell)
                newPitGroup.add(pit)
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left-CELL_SIZE, pos_y=pit.rect.top))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left+CELL_SIZE, pos_y=pit.rect.top))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left, pos_y=pit.rect.top-CELL_SIZE))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left, pos_y=pit.rect.top+CELL_SIZE))
                pitGroups.add(newPitGroup)

            if 'W' in map[i][j]:
                newMonsterGroup = pygame.sprite.Group()
                monster = Object("Graphics\\zombie_ogre.png", new_cell)
                newMonsterGroup.add(monster)
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left-CELL_SIZE, pos_y=monster.rect.top))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left+CELL_SIZE, pos_y=monster.rect.top))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left, pos_y=monster.rect.top-CELL_SIZE))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left, pos_y=monster.rect.top+CELL_SIZE))
                monsterGroups.add(newMonsterGroup)



    # Player Group
    playerGroup = pygame.sprite.Group()
    player = Player("Graphics\\paladin.png", cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[0]-1, agent.agentLoc[1]-1, map.size())])
    playerGroup.add(player)
    
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.flip()
        cellGroup.draw(screen)
        cellGroup.update()

        
        monsterGroups.draw(screen)
        monsterGroups.update()

        pitGroups.draw(screen)
        pitGroups.update()


        playerGroup.draw(screen)
        playerGroup.update()

        clock.tick(120)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()