from apq import *

class Grid:

    def __init__(self, rows, cols):
        self.structure = [[Cell(x, y) for x in range(cols)]for y in range(rows)]
        self.get_neighbours()

    def get_neighbours(self):
        for y in range(len(self.structure)):
            for x in range(len(self.structure[y])):
                if x > 0:
                    self.structure[y][x].neighbours[(y, x-1)] = 1
                if y > 0:
                    self.structure[y][x].neighbours[(y-1, x)] = 1
                if x < len(self.structure[y])-1:
                    self.structure[y][x].neighbours[(y, x+1)] = 1
                if y < len(self.structure)-1:
                    self.structure[y][x].neighbours[(y+1, x)] = 1
                if y > 0 and x > 0:
                    self.structure[y][x].neighbours[(y-1, x-1)] = 2
                if y > 0 and x < len(self.structure[y])-1:
                    self.structure[y][x].neighbours[(y-1, x+1)] = 2
                if y < len(self.structure)-1 and x < len(self.structure[y])-1:
                    self.structure[y][x].neighbours[(y+1, x+1)] = 2
                if y < len(self.structure)-1 and x > 0:
                    self.structure[y][x].neighbours[(y+1, x-1)] = 2
    
class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = {}

    def __str__(self):
        outstr = f"{self.x}, {self.y}"

    


def dijkstra(matrix, source, destination):

    open = APQ()
    closed = {}
    locs = {}
    preds = {source: None}

    elt = open.add(0, source)
    locs[source] = elt
    while open.length() != 0:
        min = open.remove_min()
        minElt = min.value
        minCost = min.key
        predecessor = preds.pop(minElt)
        closed[minElt] = (minCost, predecessor)
        if minElt == destination:
            return closed
        for cellLocation in matrix.structure[minElt[0]][minElt[1]].neighbours:
            neighbourCell = cellLocation
            if neighbourCell not in closed and neighbourCell[0] >= 0 and neighbourCell[1] > 0:
                newcost = minCost + matrix.structure[minElt[0]][minElt[1]].neighbours[neighbourCell]
                if neighbourCell not in locs:
                    preds[neighbourCell] = minElt
                    elt = open.add(newcost, neighbourCell)
                    locs[neighbourCell] = elt
                elif newcost < locs[neighbourCell].key:
                    preds[neighbourCell] = minElt
                    locs[neighbourCell].key = newcost
    return closed

matrix = Grid(5, 5)
print(dijkstra(matrix, (1, 2), (1, 4)))