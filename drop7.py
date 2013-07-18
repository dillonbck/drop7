import pygame, sys, os
from pygame.locals import *
from random import randint

##### Global variables #####
new_block = 0
BLACK = (0, 0, 0)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WIDGET_WIDTH = WIDGET_HEIGHT = 32
DROP_X = 3
DROP_Y = 0
icon_arr = [pygame.image.load("icons/"+str(z+1)+".png") for z in range(7)]

##### Class declarations #####

class Widget:
    def __init__(self, screen):
        self.number = randint(1,7)
        self.loc_x = DROP_X
        self.loc_y = DROP_Y
        self.active = 1
        self.delete = 0
        self.sprite = icon_arr[self.number - 1]
        self.draw(screen)

    def clear(self, screen):
        box = pygame.Rect(self.loc_x * WIDGET_WIDTH, self.loc_y * WIDGET_HEIGHT, WIDGET_WIDTH, WIDGET_HEIGHT)
        pygame.draw.rect(screen, BLACK, box, 0)

    def draw(self, screen):
        screen.blit(self.sprite, (self.loc_x * WIDGET_WIDTH, self.loc_y * WIDGET_HEIGHT))

    def right(self, screen, board):
        if self.loc_x < 6 and self.active == 1:
            self.clear(screen)
            self.loc_x += 1
            self.draw(screen)

    def left(self, screen, board):
        if self.loc_x >= 1 and self.active == 1:
            self.clear(screen)
            self.loc_x -= 1
            self.draw(screen)
    
    def drop(self, screen, board):
        if self.active == 1:
            if board.arr[self.loc_y + 1][self.loc_x] != None:
                return False
            self.clear(screen)
            while self.loc_y < 7 and board.arr[self.loc_y + 1][self.loc_x] == None:
                self.loc_y += 1
            board.arr[self.loc_y][self.loc_x] = self
            self.draw(screen)
            self.active = 0
            return True

    def mark(self, screen, board):
        self.delete = 1
        self.clear()
# end Widget class

class Board:
    arr = [[None for x in range(7)] for y in range(8)]

    def check_cell(self, x, y):
        if self.arr[y][x] == None:
            return False
        length = 1

        # Check horizontal
        i = x - 1
        while i >= 0 and self.arr[y][i] != None:
            length += 1
            i -= 1
        i = x + 1
        while i <= 6 and self.arr[y][i] != None:
            length += 1
            i += 1
        if length == self.arr[y][x].number:
            self.arr[y][x].mark
            return True

        # Check vertical
        i = y - 1
        length = 0
        while i >= 1 and self.arr[i][x] != None:
            length += 1
            i -= 1
        i = y + 1
        while i <= 7 and self.arr[i][x] != None:
            length += 1
            i += 1
        if length == self.arr[y][x].number:
            self.arr[y][x].mark
            return True
        return False

    def clean(self):
        boardChanged = False
        for x in range(7):
            for y in range(1, 8):
                if self.arr[y][x] != None and self.arr[y][x].delete == 1:
                    boardChanged = True
                    self.arr[y][x] = None
        #if boardChanged == True
        

    def check(self):
        boardChanged = False
        for x in range(7):
            for y in range(1, 8):
                if self.check_cell(x, y) == True:
                    boardChanged = True
        if boardChanged == True:
            self.clean()
# end Board class

##### Game stuff #####
pygame.init()                   # Initialization
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480), DOUBLEBUF)
pygame.display.set_caption('Drop7')

board = Board()
one_widget = Widget(screen)

while 1:
    clock.tick(30)

    # User Input
    for event in pygame.event.get():
        if not hasattr(event, 'key'):
            continue
        if not hasattr(event, 'unicode'):
            continue
        if event.key == K_RIGHT:
            one_widget.right(screen, board)
        elif event.key == K_LEFT:
            one_widget.left(screen, board)
        elif event.key == K_DOWN:
            if one_widget.drop(screen, board) == True:
                one_widget = Widget(screen)
                board.check()
        elif event.key == K_ESCAPE: 
            sys.exit(0)

    # Rendering
    pygame.display.flip()
