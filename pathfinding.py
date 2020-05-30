from apq import *
import math
import pygame as pg
from pygame.locals import *
from settings import *

# Creates a matrix of Cell objects and gives each cell a reference to all its neighbours
class Grid:

    def __init__(self, rows, cols):
        # A matrix of cell objects
        self.structure = [[Cell(x, y) for x in range(cols)]for y in range(rows)]
        self.get_neighbours()

    # Gives each cell references to its neighbours and prevents the indices from going out of range
    # If a neighbour is diagonally positioned from a cell then the cost to get to the neighbour is 2
    # Else its a cost of 1
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
        self.in_open = False
        self.in_closed = False
        self.cell_size = CELL_SIZE
        self.blocked = False

    def __str__(self):
        outstr = f"{self.x}, {self.y}"
        return outstr

    def draw_cell(self):
        if not self.blocked:
            if self.in_open:
                pg.draw.rect(screen, YELLOW, (self.x*self.cell_size+self.x, self.y*self.cell_size+self.y, self.cell_size, self.cell_size))
            elif self.in_closed:
                pg.draw.rect(screen, RED, (self.x*self.cell_size+self.x, self.y*self.cell_size+self.y, self.cell_size, self.cell_size))
            else:
                pg.draw.rect(screen, WHITE, (self.x*self.cell_size+self.x, self.y*self.cell_size+self.y, self.cell_size, self.cell_size))
        else:
            pg.draw.rect(screen, BLACK, (self.x*self.cell_size+self.x, self.y*self.cell_size+self.y, self.cell_size, self.cell_size))

def run(source, dest):
        running = True
        draw()
        while running:
            for event in pg.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        dijkstra(source, dest)
                elif event.type == MOUSEBUTTONDOWN:
                    position = pg.mouse.get_pos()
                    block(position)
        pg.quit()  

def draw():
    screen.fill(BLACK)
    for i in range(len(grid.structure)):
        for j in range(len(grid.structure[i])):
            grid.structure[i][j].draw_cell()
    pg.display.flip()


def trace_path(index, closed):
    if index == None:
        return True
    else:
        index_x = index[1]
        index_y = index[0]
        cell_size = grid.structure[index_y][index_x].cell_size
        pg.draw.rect(screen, BLUE, (index_x*cell_size+index_x, index_y*cell_size+index_y, cell_size, cell_size))
        pg.display.flip()
        pg.time.delay(100)
        trace_path(closed[index][1], closed)

def block(position):
        x = position[0]
        y = position[1]
        row = math.ceil(y // CELL_SIZE) - 1
        col = math.ceil(x // CELL_SIZE) - 1
        cell = grid.structure[row][col]
        cell.blocked = True
        draw()


#Implementation of dijkstra using my own implementation of a min binary heap for the open cells
# Locs stores the references to the open cells in the priority queue so that the algorithm can check whether
# A cell is in open
def dijkstra(source, destination):

    open = APQ()
    closed = {}
    locs = {}
    preds = {source: None}

    elt = open.add(0, source)
    locs[source] = elt
    grid.structure[source[0]][source[1]].in_open = True
    draw()
    while open.length() != 0:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
        min = open.remove_min()
        minElt = min.value
        minCost = min.key
        min_cell = grid.structure[minElt[0]][minElt[1]]
        locs.pop(minElt)
        predecessor = preds.pop(minElt)
        closed[minElt] = (minCost, predecessor)
        min_cell.in_open = False
        min_cell.in_closed = True
        draw()
        if minElt == destination:
            trace_path(destination, closed)
            return closed
        for cellLocation in grid.structure[minElt[0]][minElt[1]].neighbours:
                neighbour_cell_obj = grid.structure[cellLocation[0]][cellLocation[1]]
                if not neighbour_cell_obj.in_closed and not neighbour_cell_obj.blocked:
                    newcost = minCost + grid.structure[minElt[0]][minElt[1]].neighbours[cellLocation]
                    if cellLocation not in locs:
                        preds[cellLocation] = minElt
                        elt = open.add(newcost, cellLocation)
                        locs[cellLocation] = elt
                        neighbour_cell_obj.in_open = True
                        draw()
                    elif newcost < locs[cellLocation].key:
                        preds[neighbourCell] = minElt
                        locs[neighbourCell].key = newcost
                        draw()

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
grid = Grid(ROWS, COLS)

def main():
    run((2, 7), (20, 20))

main()