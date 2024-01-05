from zmq import proxy
from functions import *
from agent import Agent
from map import Map
from constants import *
import sys
import pygame
from Object import Cell
from Player import Player
from Object import Object
from constants import CELL_SIZE

def getCellIDinGroup(pos_x: int, pos_y: int, map_size: int):
    # print(pos_x, pos_y, map_size, pos_x - 1 + (map_size - pos_y) * map_size)
    return pos_x - 1 + (map_size - pos_y) * map_size

def main():
    agent = Agent()
    map, agent.agentLoc = input("tests/test2.txt")

    loop_n = map.size() + 1 # true loop size, not map's size
    for y in range(loop_n-1, 0, -1):
        for x in range(1, loop_n):
            print(map[y][x], end=",")
        print()


    # while agent.isAlive and not agent.isEscaping:
    #     # print('===========================', agent.agentLoc)
    #     agent.perceiveEnvironment(map)
    #     # print('kb: ', agent.kb.clauses)

    #     nextRoom = agent.findASafeStep(map.size())
    #     if nextRoom == [-1, -1]:
    #         nextRoom, isShooting, maybePit = agent.forceAStep(map.size())
    #         print('isShooting', isShooting)
    #         if maybePit and agent.foundExit:
    #             nextRoom = [1, 1]
    #             agent.isEscaping = True
    #             print('escapse')

    #     print(nextRoom)

    #     agent.playPath(nextRoom)
    #     agent.agentLoc = nextRoom

    # General initializations
    pygame.display.set_caption('Wumpus World')
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("freesansbold" , 18 , bold = True)

    # Game screen
    screen_width = map.size() * CELL_SIZE
    screen_height = map.size() * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

    # Pits Group
    pitGroups = pygame.sprite.Group()

    # Monster Group
    monsterGroups = pygame.sprite.Group()

    # Gold Group
    goldGroup = pygame.sprite.Group()

    # Fog of War Group
    fogGroup = pygame.sprite.Group()

    # Cell Group
    cellGroup = pygame.sprite.Group()
    for y in range(loop_n-1, 0, -1):
        for x in range(1, loop_n):
            new_cell = Cell("Graphics\\catacombs_", CELL_SIZE/2 + CELL_SIZE * (x-1), CELL_SIZE/2 + CELL_SIZE * (loop_n - 1 - y))
            cellGroup.add(new_cell)
            fogGroup.add(new_cell.fog)
            
            if 'P' in map[y][x]:
                newPitGroup = pygame.sprite.Group()
                pit = Object("Graphics\\trap_arrow.png", new_cell)
                newPitGroup.add(pit)
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left-CELL_SIZE, pos_y=pit.rect.top))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left+CELL_SIZE, pos_y=pit.rect.top))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left, pos_y=pit.rect.top-CELL_SIZE))
                newPitGroup.add(Object("Graphics\\air_magic.png", pos_x=pit.rect.left, pos_y=pit.rect.top+CELL_SIZE))
                pitGroups.add(newPitGroup)

            if 'W' in map[y][x]:
                newMonsterGroup = pygame.sprite.Group()
                monster = Object("Graphics\\zombie_ogre.png", new_cell)
                newMonsterGroup.add(monster)
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left-CELL_SIZE, pos_y=monster.rect.top))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left+CELL_SIZE, pos_y=monster.rect.top))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left, pos_y=monster.rect.top-CELL_SIZE))
                newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", pos_x=monster.rect.left, pos_y=monster.rect.top+CELL_SIZE))
                monsterGroups.add(newMonsterGroup)

            if 'G' in map[y][x]:
                newGold = Object("Graphics\\chest.png", new_cell)
                goldGroup.add(newGold)

    # Exit door
    cellGroup.add(Object("Graphics\\closed_door.png", cellGroup.sprites()[getCellIDinGroup(1, 1, map.size())]))
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(1, 1, map.size())].fog)

    # Player Group
    playerGroup = pygame.sprite.Group()
    player = Player("Graphics\\paladin.png", cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())])
    playerGroup.add(player)
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

    # Misc
    pause = True
    fog = True
    
    # Main game loop
    while agent.isAlive and not agent.isEscaping:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # print("pause changed")
                    pause = not pause
                if event.key == pygame.K_f:
                    fog = not fog
        
        if not pause:
            # print('===========================', agent.agentLoc)
            agent.perceiveEnvironment(map)
            # print('kb: ', agent.kb.clauses)

            nextRoom = agent.findASafeStep(map.size())
            if nextRoom == [-1, -1]:
                nextRoom, isShooting, maybePit = agent.forceAStep(map.size())
                print('isShooting', isShooting)
                if maybePit and agent.foundExit:
                    nextRoom = [1, 1]
                    agent.isEscaping = True
                    print('escape')

            print(nextRoom)

            player.play_path(cellGroup.sprites()[getCellIDinGroup(nextRoom[1], nextRoom[0], map.size())])
            agent.agentLoc = nextRoom

            fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

            print(agent.visited)

            pause = not pause

        cellGroup.draw(screen)
        cellGroup.update()

        
        monsterGroups.draw(screen)
        monsterGroups.update()

        pitGroups.draw(screen)
        pitGroups.update()

        goldGroup.draw(screen)
        goldGroup.update()

        playerGroup.draw(screen)
        playerGroup.update()

        if fog:
            fogGroup.draw(screen)
            fogGroup.update()

        pygame.display.flip()

        clock.tick(120)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()