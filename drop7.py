import pygame, sys, os
from pygame.locals import *
from random import randint

##### Global variables #####
new_block = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
            while self.loc_y < 7 and board.arr[self.loc_y + 1][self.loc_x] == None:
                self.clear(screen)
                self.loc_y += 1
                self.draw(screen)
                pygame.time.wait(100)
                pygame.display.flip()
            board.arr[self.loc_y][self.loc_x] = self
            self.active = 0
            return True

    def mark(self, screen, board):
        self.delete = 1
        self.clear(screen)
# end Widget class

class Board:
    arr = [[None for x in range(7)] for y in range(8)]
    modifier = 1
    score = 0

    def check_cell(self, x, y):
        if self.arr[y][x] == None:
            return False

        # Check horizontal
        length = 1
        i = x - 1
        while i >= 0 and self.arr[y][i] != None:
            length += 1
            i -= 1
        i = x + 1
        while i <= 6 and self.arr[y][i] != None:
            length += 1
            i += 1
        if length == self.arr[y][x].number:
            self.arr[y][x].mark(screen, board)
            return True

        # Check vertical
        i = y - 1
        length = 1
        while i >= 1 and self.arr[i][x] != None:
            length += 1
            i -= 1
        i = y + 1
        while i <= 7 and self.arr[i][x] != None:
            length += 1
            i += 1
        if length == self.arr[y][x].number:
            self.arr[y][x].mark(screen, board)
            return True
        return False

    def scoot(self, screen):
        boardChanged = False
        for x in range(7):
            for y in range(1, 7):
                if self.arr[y][x] != None and self.arr[y + 1][x] == None:
                    myWidget = self.arr[y][x]
                    myWidget.clear(screen)
                    myWidget.loc_y += 1
                    self.arr[y + 1][x] = myWidget
                    self.arr[y][x] = None
                    myWidget.draw(screen)
                    boardChanged = True
        return boardChanged

    def clean(self):
        boardChanged = False
        for x in range(7):
            for y in range(1, 8):
                if self.arr[y][x] != None and self.arr[y][x].delete == 1:
                    self.score += pow(7, self.modifier) 
                    boardChanged = True
                    self.arr[y][x].clear(screen)
                    self.arr[y][x] = None
        return boardChanged
        
    def printScore(self, screen):
        text = font.render("Score: " + str(self.score), 1, WHITE)
        textpos = text.get_rect(left=250)
        pygame.draw.rect(screen, BLACK, textpos)
        screen.blit(text, textpos)

    def check(self, screen):
        boardChanged = False
        for x in range(7):
            for y in range(1, 8):
                if self.check_cell(x, y) == True:
                    boardChanged = True
        pygame.time.wait(50)
        if self.clean() == True:
            boardChanged = True
        pygame.time.wait(50)
        if self.scoot(screen) == True:
            boardChanged = True

        if boardChanged == True:
            self.printScore(screen)
            self.check(screen)
# end Board class

##### Game stuff #####
pygame.init()                   # Initialization
clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480), DOUBLEBUF)
pygame.display.set_caption('Drop7')
font = pygame.font.Font(None, 12)

board = Board()
active_widget = Widget(screen)

while 1:
    clock.tick(30)

    # User Input
    for event in pygame.event.get():
        if not hasattr(event, 'key'):
            continue
        if not hasattr(event, 'unicode'):
            continue
        if event.key == K_RIGHT:
            active_widget.right(screen, board)
        elif event.key == K_LEFT:
            active_widget.left(screen, board)
        elif event.key == K_DOWN:
            if active_widget.drop(screen, board) == True:
                active_widget = Widget(screen)
                board.check(screen)
        elif event.key == K_ESCAPE or event.key == K_q: 
            sys.exit(0)

    # Rendering
    pygame.display.flip()
