R = [-1, 0, 1, 0]
C = [0, -1, 0, 1]

def input(filePath):
    with open(filePath, 'r') as file:
        n = int(file.readline().splitlines()[0])
        map = []
        map.append(['' for i in range(n + 2)])
        for i in range(n):
            line = '.' + file.readline().splitlines()[0] + '.'
            map.append(line.replace('-', '').split('.'))
        map.append(['' for i in range(n + 2)])

    agentCoord = [0, 0]
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if 'A' in map[i][j]:
                agentCoord = [i, j]
                map[i][j].replace('A', '')
            for k in range(4):
                if map[i + R[k]][j + C[k]] == 'P' and 'B' not in map[i][j]:
                    map[i][j] += 'B'
                if map[i + R[k]][j + C[k]] == 'W' and 'S' not in map[i][j]:
                    map[i][j] += 'S'
                
    return map, agentCoord
# map = input('tests/test1.txt')
# print(map)

