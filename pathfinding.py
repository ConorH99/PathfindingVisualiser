import math
import sys
import pygame as pg
from pygame.locals import *
import tkinter as tk
from tkinter import messagebox as mb
from apq import *
from settings import *

pg.init()

# Creates a matrix of Cell objects and gives each cell a reference to all its neighbours
class Grid:

    def __init__(self, screen, rows, cols):
        # A matrix of cell objects
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.structure = [[Cell(x, y) for x in range(cols)]for y in range(rows)]
        self.generate_neighbours()

    # Gives each cell references to its neighbours and prevents the list indices from going out of range
    # If a neighbour is diagonally positioned from a cell then the cost to get to the neighbour is 2
    # Else its a cost of 1
    def generate_neighbours(self):
        for y in range(len(self.structure)):
            for x in range(len(self.structure[y])):
                cell = self.structure[y][x]
                if x > 0:
                    cell.get_left()
                if y > 0:
                    cell.get_top()
                if x < len(self.structure[y])-1:
                    cell.get_right()
                if y < len(self.structure)-1:
                    cell.get_bottom()
                if y > 0 and x > 0:
                    cell.get_top_left()
                if y > 0 and x < len(self.structure[y])-1:
                    cell.get_top_right()
                if y < len(self.structure)-1 and x < len(self.structure[y])-1:
                    cell.get_bottom_right()
                if y < len(self.structure)-1 and x > 0:
                    cell.get_bottom_left()
                    

    
class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = {}
        self.in_open = False
        self.in_closed = False
        self.cell_size = CELL_SIZE
        self.blocked = False
        self.is_source = False
        self.is_dest = False

    def __str__(self):
        outstr = f"{self.x}, {self.y}"
        return outstr

    def draw_cell(self, screen):
        if not self.is_source and not self.is_dest:
            self.draw_dijkstra(screen)
        else:
            if self.is_source:
                self.cell_rect(screen, GREEN)
            elif self.is_dest:
                self.cell_rect(screen, BLUE)

    def draw_dijkstra(self, screen):
        if not self.blocked:
                if self.in_open:
                    self.cell_rect(screen, YELLOW)
                elif self.in_closed:
                    self.cell_rect(screen, RED)
                elif self.is_source:
                    self.cell_rect(screen, BLUE)
                elif self.is_dest:
                    self.cell_rect(screen, GREEN)
                else:
                    self.cell_rect(screen, WHITE)
        else:
            self.cell_rect(screen, BLACK)

    def cell_rect(self, screen, colour):
        x_pos = self.x*self.cell_size+self.x
        y_pos = self.y*self.cell_size+self.y
        width = self.cell_size
        height = self.cell_size
        pg.draw.rect(screen, colour, (x_pos, y_pos, width, height ))
        
    def get_left(self):
        self.neighbours[(self.y, self.x-1)] = 1
    
    def get_right(self):
        self.neighbours[(self.y, self.x+1)] = 1

    def get_top(self):
        self.neighbours[(self.y-1, self.x)] = 1

    def get_bottom(self):
        self.neighbours[(self.y+1, self.x)] = 1

    def get_top_left(self):
        self.neighbours[(self.y-1, self.x-1)] = 2

    def get_top_right(self):
        self.neighbours[(self.y-1, self.x+1)] = 2

    def get_bottom_left(self):
        self.neighbours[(self.y+1, self.x-1)] = 2

    def get_bottom_right(self):
        self.neighbours[(self.y+1, self.x+1)] = 2

class Tkinter_GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.start_end_frame = tk.Frame(self.window)
        self.start_end_frame.pack()
        self.start_lbl = tk.Label(self.start_end_frame, text="Enter start coordinates:")
        self.end_lbl = tk.Label(self.start_end_frame, text="Enter end coordinates:")
        self.start_entry = tk.Entry(self.start_end_frame)
        self.end_entry = tk.Entry(self.start_end_frame)
        self.submit_btn = tk.Button(self.start_end_frame, text="Submit", command=self.on_submit)
        self.start_lbl.pack()
        self.start_entry.pack()
        self.end_lbl.pack()
        self.end_entry.pack()
        self.submit_btn.pack()
        self.source = None
        self.dest = None
        tk.mainloop()

    def on_submit(self):
        while True:
            try:
                source = tuple(map(int, self.start_entry.get().split(",")))
                dest = tuple(map(int, self.end_entry.get().split(",")))
                break
            except:
                mb.showerror("ERROR!", "Start and end should be in the form\nint, int")
                self.window.destroy()
                main()
        
        self.source = source
        self.dest = dest
        self.window.destroy()

def run(screen, grid, source, dest):
    grid.structure[source[0]][source[1]].is_source = True
    grid.structure[dest[0]][dest[1]].is_dest = True
    running = True
    draw(screen, grid)
    while running:
        pressed = pg.mouse.get_pressed()
        if pressed[0]:
            position = pg.mouse.get_pos()
            block(screen, grid, position)
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    dijkstra(screen, grid, source, dest)
                    wait()
                    running = False
    pg.quit()  

def draw(screen, grid):
    screen.fill(BLACK)
    for i in range(len(grid.structure)):
        for j in range(len(grid.structure[i])):
            grid.structure[i][j].draw_cell(screen)
    pg.display.flip()

def trace_path(screen, grid, index, closed):
    if index == None:
        return True
    else:
        index_x = index[1]
        index_y = index[0]
        cell = grid.structure[index_y][index_x]
        cell.cell_rect(screen, BLUE)
        pg.display.flip()
        pg.time.delay(100)
        trace_path(screen, grid, closed[index][1], closed)

def block(screen, grid, position):
        x = position[0]
        y = position[1]
        row = math.ceil(y // CELL_SIZE) - 1
        col = math.ceil(x // CELL_SIZE) - 1
        try:
            cell = grid.structure[row][col]
            cell.blocked = True
            draw(screen, grid)
        except IndexError:
            pass
def wait():
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == QUIT:
                waiting = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    waiting = False
                    main()


#Implementation of dijkstra using my own implementation of a min binary heap for the open cells
# Locs stores the references to the open cells in the priority queue so that the algorithm can check whether
# A cell is in open
def dijkstra(screen, grid, source, destination):

    open = APQ()
    closed = {}
    locs = {}
    preds = {source: None}

    elt = open.add(0, source)
    locs[source] = elt
    grid.structure[source[0]][source[1]].in_open = True
    draw(screen, grid)
    while open.length() != 0:
        for event in pg.event.get():
            if event.type == QUIT:
                sys.exit()
        min = open.remove_min()
        minElt = min.value
        minCost = min.key
        min_cell = grid.structure[minElt[0]][minElt[1]]
        locs.pop(minElt)
        predecessor = preds.pop(minElt)
        closed[minElt] = (minCost, predecessor)
        min_cell.in_open = False
        min_cell.in_closed = True
        draw(screen, grid)
        if minElt == destination:
            trace_path(screen, grid, destination, closed)
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
                        draw(screen, grid)
                    elif newcost < locs[cellLocation].key:
                        preds[neighbourCell] = minElt
                        locs[neighbourCell].key = newcost
                        draw(screen, grid)
    mb.showerror("ERROR!", "No path available")
    return False

def main():

    start_gui = Tkinter_GUI()
    pg.display.set_caption("PATHFINDING")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    grid = Grid(screen, ROWS, COLS)
    run(screen, grid, start_gui.source, start_gui.dest)

main()