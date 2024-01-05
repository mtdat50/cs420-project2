from agent import Agent
from map import Map
from constants import *
import sys
import pygame
from Object import Cell
from Player import Player
from Object import Object, Arrow
from constants import CELL_SIZE
from sys import argv 
import reward

def getCellIDinGroup(pos_x: int, pos_y: int, map_size: int):
    # print(pos_x, pos_y, map_size, pos_x - 1 + (map_size - pos_y) * map_size)
    return pos_x - 1 + (map_size - pos_y) * map_size

def check_breeze_stench_overwritting(cell_info):
    if 'W' in cell_info:
        return False
    if 'A' in cell_info:
        return False
    if 'P' in cell_info:
        return False
    
    return True

def main():
    agent = Agent()
    # map, agent.agentLoc = input("tests/test"+argv[1]+".txt")
    map, agent.agentLoc = Map.input("tests/test10.txt")

    loop_n = map.size() + 1 # true loop size, not map's size
    for y in range(loop_n-1, 0, -1):
        for x in range(1, loop_n):
            print(map[y][x], end=",")
        print()

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
            new_cell = Cell(CELL_SIZE * (x-1),CELL_SIZE * (loop_n - 1 - y), initial_scale=INIT_ZOOM)
            cellGroup.add(new_cell)
            fogGroup.add(new_cell.fog)
            
            if 'P' in map[y][x]:
                newPitGroup = pygame.sprite.Group()
                pit = Object("Graphics\\trap_arrow.png", new_cell, initial_scale=INIT_ZOOM)
                newPitGroup.add(pit)
                if check_breeze_stench_overwritting(map[y][x-1]):
                    newPitGroup.add(Object("Graphics\\air_magic.png", cell_center=(pit.rect.center[0]-CELL_SIZE, pit.rect.center[1]), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y][x+1]):
                    newPitGroup.add(Object("Graphics\\air_magic.png", cell_center=(pit.rect.center[0]+CELL_SIZE, pit.rect.center[1]), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y-1][x]):
                    newPitGroup.add(Object("Graphics\\air_magic.png", cell_center=(pit.rect.center[0], pit.rect.center[1]+CELL_SIZE), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y+1][x]):
                    newPitGroup.add(Object("Graphics\\air_magic.png", cell_center=(pit.rect.center[0], pit.rect.center[1]-CELL_SIZE), initial_scale=1.5))
                pitGroups.add(newPitGroup)

            if 'W' in map[y][x]:
                newMonsterGroup = pygame.sprite.Group()
                monster = Object("Graphics\\zombie_ogre.png", new_cell, initial_scale=INIT_ZOOM)
                newMonsterGroup.add(monster)
                if check_breeze_stench_overwritting(map[y][x-1]):
                    newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", cell_center=(monster.rect.center[0]-CELL_SIZE, monster.rect.center[1]), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y][x+1]):
                    newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", cell_center=(monster.rect.center[0]+CELL_SIZE, monster.rect.center[1]), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y-1][x]):
                    newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", cell_center=(monster.rect.center[0], monster.rect.center[1]+CELL_SIZE), initial_scale=1.5))
                if check_breeze_stench_overwritting(map[y+1][x]):
                    newMonsterGroup.add(Object("Graphics\\cloud_poison_1.png", cell_center=(monster.rect.center[0], monster.rect.center[1]-CELL_SIZE), initial_scale=1.5))
                monsterGroups.add(newMonsterGroup)

            if 'G' in map[y][x]:
                newGold = Object("Graphics\\chest.png", new_cell, initial_scale=INIT_ZOOM)
                goldGroup.add(newGold)

    # Exit door
    doorGroup = pygame.sprite.Group()
    doorGroup.add(Object("Graphics\\closed_door.png", cellGroup.sprites()[getCellIDinGroup(1, 1, map.size())], initial_scale=INIT_ZOOM))
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(1, 1, map.size())].fog)

    # Player Group
    playerGroup = pygame.sprite.Group()
    player = Player("Graphics\\paladin.png", cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())], initial_scale=1.5)
    playerGroup.add(player)
    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

    arrowGroup = pygame.sprite.Group()

    # Misc
    pause = True
    fog = True
    
    path = []
    isShooting = False
    waiting_for_arrow = False
    # Main game loop
    while (agent.isAlive and not agent.isEscaping) or len(path) != 0:
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
        
        if not pause and not waiting_for_arrow:
            if len(path) == 0:
                # print('===========================', agent.agentLoc)
                agent.perceiveEnvironment(map)
                # print('kb: ', agent.kb.clauses)

                # if (agent.agentLoc[0], agent.agentLoc[1]) == (2, 9):
                #     o = 0
                nextRoom = agent.findASafeStep(map.size())
                isShooting = False
                if nextRoom == [-1, -1]:
                    nextRoom, isShooting, maybePit = agent.forceAStep(map.size())
                    print('isShooting', isShooting)
                    print('maybePit', maybePit)
                    if maybePit and agent.foundExit:
                        nextRoom = [1, 1]
                        agent.isEscaping = True
                        print('escape')

                print(nextRoom)
                path = agent.playPath(nextRoom)
                if (nextRoom[0], nextRoom[1]) == (2, 9):
                    o = 0

            if len(path) != 0:
                agent.point += reward.PUNISHMENT_FOR_MOVING
                nextRoom = path[0]
                path.pop(0)
                if len(path) == 0 and isShooting:
                    agent.shoot(nextRoom, map)
                    # Shoot wumpus
                    arrow = Arrow(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].rect,
                                   cellGroup.sprites()[getCellIDinGroup(nextRoom[1], nextRoom[0], map.size())])
                    arrowGroup.add(arrow)
                    waiting_for_arrow = True
                if not waiting_for_arrow:
                    player.play_path(cellGroup.sprites()[getCellIDinGroup(nextRoom[1], nextRoom[0], map.size())])
                    agent.agentLoc = nextRoom
                    fogGroup.remove(cellGroup.sprites()[getCellIDinGroup(agent.agentLoc[1], agent.agentLoc[0], map.size())].fog)

            pause = not pause

                

        cellGroup.draw(screen)
        cellGroup.update()

        
        monsterGroups.draw(screen)
        monsterGroups.update()

        pitGroups.draw(screen)
        pitGroups.update()

        doorGroup.draw(screen)
        doorGroup.update()

        goldGroup.draw(screen)
        goldGroup.update()

        playerGroup.draw(screen)
        playerGroup.update()

        if fog:
            fogGroup.draw(screen)
            fogGroup.update()

        arrowGroup.draw(screen)
        arrowGroup.update()

        if waiting_for_arrow:
            # Check if the arrow has reached the target cell
            if arrowGroup.sprites()[0].reached_target:
                waiting_for_arrow = False
                print("Arrow reached the target cell!")
                arrowGroup.remove(arrowGroup.sprites()[0])

        pygame.display.flip()

        clock.tick(120)

def updateMap(shotRoomCoord):
    pass

if __name__ == "__main__":
    main()