from turtle import update


R = [-1, 0, 1, 0]
C = [0, -1, 0, 1]

def updateInfo(self):
    n = self.size()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(4):
                if self[i + R[k]][j + C[k]] == 'P' and 'B' not in self[i][j]:
                    self[i][j] += 'B'
                if self[i + R[k]][j + C[k]] == 'W' and 'S' not in self[i][j]:
                    self[i][j] += 'S'
    

def input(filePath):
    with open(filePath, 'r') as file:
        n = int(file.readline().splitlines()[0])
        map = []
        map.append(['' for i in range(n + 2)])
        for i in range(n):
            line = '.' + file.readline().splitlines()[0] + '.'
            map.append(line.replace('-', '').split('.'))
        map.append(['' for i in range(n + 2)])

    map.reverse()
    
    agentLoc = [0, 0]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if 'A' in map[i][j]:
                agentLoc = [i, j]
                i = n + 1
                break

    map = Map(n, map)
    map.updateInfo()
    return Map(n, map), agentLoc
# map = input('tests/test1.txt')
# print(map)


class Map():
    def __init__(self, n = 0, map = []):
        self.__size = n
        self.__map = map
        if n != 0 and map == []:
            map = [[[''] for c in range(n + 3)] for r in range(n + 3)]
    
    def __getitem__(self, row):
        return self.__map[row]
    
    def __setitem__(self, row, data):
        self.__map[row] = data
    
    def size(self):
        return self.__size
    
    updateInfo = updateInfo
    input = input