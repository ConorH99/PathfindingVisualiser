from apq import *
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

class GUI:

    def __init__(self, num_rows, num_cols):
        pg.init()
        self.grid = Grid(num_rows, num_cols)
        self.cell_size = CELL_SIZE
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_ver = (15, 15)
        self.target_ver = (20, 20)
        
    def run(self):
        self.running = True
        while self.running:
            self.events()
        pg.quit()

    def draw(self):
        self.screen.fill(BLACK)
        for i in range(len(self.grid.structure)):
            for j in range(len(self.grid.structure[i])):
                if (j, i) in self.grid.locs:
                    pg.draw.rect(self.screen, YELLOW, (j*self.cell_size+j, i*self.cell_size+i, self.cell_size, self.cell_size))
                if (j, i) in self.grid.closed:
                    pg.draw.rect(self.screen, RED, (j*self.cell_size+j, i*self.cell_size+i, self.cell_size, self.cell_size))
                if (j, i) not in self.grid.closed and (j, i) not in self.grid.locs:
                    pg.draw.rect(self.screen, WHITE, (j*self.cell_size+j, i*self.cell_size+i, self.cell_size, self.cell_size))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.dijkstra((1, 2), (20, 20))

    def trace_path(self, index):
        if index == None:
            return True
        else:
            index_x = index[1]
            index_y = index[0]
            pg.draw.rect(self.screen, BLUE, (index_y*self.cell_size+index_y, index_x*self.cell_size+index_x, self.cell_size, self.cell_size))
            pg.display.flip()
            pg.time.delay(100)
            self.trace_path(self.grid.closed[index][1])

    #Implementation of dijkstra using my own implementation of a min binary heap for the open cells
    # Locs stores the references to the open cells in the priority queue so that the algorithm can check whether
    # A cell is in open
    def dijkstra(self, source, destination):

        self.grid.open = APQ()
        self.grid.closed = {}
        self.grid.locs = {}
        self.grid.preds = {source: None}

        elt = self.grid.open.add(0, source)
        self.grid.locs[source] = elt
        self.draw()
        while self.grid.open.length() != 0:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
            min = self.grid.open.remove_min()
            minElt = min.value
            minCost = min.key
            self.grid.locs.pop(minElt)
            predecessor = self.grid.preds.pop(minElt)
            self.grid.closed[minElt] = (minCost, predecessor)
            self.draw()
            if minElt == destination:
                self.trace_path(self.target_ver)
                return self.grid.closed
            for cellLocation in self.grid.structure[minElt[0]][minElt[1]].neighbours:
                neighbourCell = cellLocation
                if neighbourCell not in self.grid.closed:
                    newcost = minCost + self.grid.structure[minElt[0]][minElt[1]].neighbours[neighbourCell]
                    if neighbourCell not in self.grid.locs:
                        self.grid.preds[neighbourCell] = minElt
                        elt = self.grid.open.add(newcost, neighbourCell)
                        self.grid.locs[neighbourCell] = elt
                        self.draw()
                    elif newcost < self.grid.locs[neighbourCell].key:
                        self.grid.preds[neighbourCell] = minElt
                        self.grid.locs[neighbourCell].key = newcost
                        self.draw()


    
class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = {}

    def __str__(self):
        outstr = f"{self.x}, {self.y}"
        return outstr


def main():
    gui = GUI(30, 30)
    gui.run()

main()