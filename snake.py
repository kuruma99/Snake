# Snake Tutorial Python
# Author: Mridul Singh

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20 # total rows in window
    w = 500 # size of window
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)): #dirnx = 1 so that as game starts, it starts moving in the x direction
       self.pos = start # starting position of the cube
       self.dirnx = 1 # initial direction of movement for cube
       self.dirny = 0 # initial direction of movement in y direction
       self.color = color # color for the snack


    def move(self, dirnx, dirny):
        self.dirnx = dirnx # direction of movement of cube in x direction
        self.dirny = dirny # direction of movement of cube in y direction
        self.pos= (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # repostion the cube

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # distance between two rows or columns
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2)) # draw a cube object
        if eyes: # if head of snake then config for the eyes
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis- radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius) # draw left eye
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius) # draw right eye

class snake(object):
    body = [] # body array of the snake
    turns = {} # dictionary
    def __init__(self, color, pos): # constructor
        self.color = color # assigning color of snake
        self.head = cube(pos) # assigning head of snake, as snake is made up of cubes
        self.body.append(self.head) # appending the body to the head of snake
        self.dirnx = 0 # if moving in x direction
        self.dirny = 1 # if moving in y direction

    def move(self): # function to move the snake
        for event in pygame.event.get(): # looping over all the events
            if event.type == pygame.QUIT: # checking if quit is called
                pygame.quit()

            keys = pygame.key.get_pressed() # returns all keyboard keys pressed
            
            for key in keys: # looping over all the keys pressed
                if keys[pygame.K_LEFT]: # if left key pressed
                    self.dirnx = -1 # changing the direction of x to left
                    self.dirny = 0 # no movement in y direction
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]: # if right key pressed
                    self.dirnx = 1 # changing the direction of x to right
                    self.dirny = 0 # no movement in y direction
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]: # if up key pressed
                    self.dirnx = 0 # no movement in x
                    self.dirny = -1 # movement in y direction
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]: # if down key pressed
                    self.dirnx = 0 # no x movement
                    self.dirny = 1 #  movement in y direction
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i, c in enumerate(self.body): # i is index and c is cube object in our snake body
            p = c.pos[:] # grab the position of each cube
            if p in self.turns: # see if that position is in our turns list
                turn = self.turns[p] # where to turn 
                c.move(turn[0], turn[1]) # cube.move(dirx, diry)
                if i == len(self.body) - 1: # if last cube, remove that turn
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0: # if snake goes out of left window
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: # if snake goes out of right window
                    c.pos = (0, c.pos[1])
                elif c.dirny == +1 and c.pos[1] >= c.rows-1: # if snake goes out of top
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    c.move(c.dirnx, c.dirny) # keep moving in the same direction

     

    def reset(self, pos):
        self.head = cube(pos) # reset head of snake to initial pos
        self.body = [] # clearing body
        self.body.append(self.head) # adding head to body
        self.turns = {} # clearing turns
        self.dirnx = 0 # initial x direction
        self.dirny = 1 # initial y direction

    def addCube(self):
        tail = self.body[-1] # last cube of snake body
        dx, dy = tail.dirnx, tail.dirny # direction of movement of tail

        # Appending the new cube based on the direction of tail
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # Giving the direction to added cube based on the direction of tail
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy



    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True) # if its the first cube, add eyes to it
            else: # else it is a normal cube of body
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # finding the size between the lines
    x = 0 # x coordinate
    y = 0 # y coordinate
    for i in range(rows):
        x = x + sizeBtwn # updating x coordinate via loop
        y = y + sizeBtwn # updating y coordinate via loop

        pygame.draw.line(surface, (255,255,255), (x,0), (x,w)) # drawing vertical lines
        pygame.draw.line(surface, (255,255,255), (0,y), (w,y)) # drawing horizontal lines

def redrawWindow(surface):
    global rows, width, s, snack # making these variables global so that it is accessible
    surface.fill((0,0,0)) # drawing the window, left top corner is (0,0)
    s.draw(surface) # draws the snake
    snack.draw(surface)
    drawGrid(width, rows, surface) # calls the function drawgrid to draw grid in window
    pygame.display.update()


# This function returns the coordinate for the new snack to appear
def randomSnack(rows, item): # item: snake object
    positions = item.body # new list = list of snake body

    while True:
        x = random.randrange(rows) # generating a random x coordinate
        y = random.randrange(rows) # generating a random y coordinate
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0: # making sure we don't put snack on top of the body of the snake
            continue
        else:
            break

    return(x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500 # width of the window
    rows = 20 # rows take care it divides the width
    win = pygame.display.set_mode((width, width)) # creating a window
    s = snake((255, 0, 0), (10,10)) # snake object with red color
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock() # created clock

    while flag:
        pygame.time.delay(50) # delay 50 ms so that program doesn't run too fast, lower it is faster is the game
        clock.tick(10) # the lower this is the slower is the game

        redrawWindow(win) # redraws the window
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('Game Over!', 'Your Score: {}'.format(len(s.body)))
                s.reset((10,10))
                break

        redrawWindow(win)

    pass

main()
