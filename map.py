class Map():
    def __init__(self, n, map):
        self.__size = n
        self.__map = map
    
    def __getitem__(self, row, col):
        return self.__map[row][col]
    
    def size(self):
        return self.__size