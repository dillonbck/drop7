import logging
import pygame

import config

from widget import Widget


logger = logging.getLogger(__name__)

class Board:

    def __init__(self):

        self.arr = [[None for x in range(7)] for y in range(7)]

        self.widget_count = 0

    # Check to see if the widget at the specified location will be destroyed
    def check_cell(self, x, y):

        # If cell empty, return False
        if self.arr[y][x] == None:
            return False

        # Check horizontal widget removals
        length = 1
        i = x - 1
        while i >= 0 and self.arr[y][i] != None:
            length += 1
            i -= 1
        i = x + 1
        while i <= 6 and self.arr[y][i] != None:
            length += 1
            i += 1
        if self.arr[y][x].unbroken == False and self.arr[y][x].cracked == False and length == self.arr[y][x].number:
            self.arr[y][x].remove()  # Destroy this widget
            self.widget_count -= 1

            # check if adjacent widgets are unbroken and if so crack them
            self.check_adjacent(x, y)
            return True

        # Check vertical widget removals
        i = y - 1
        length = 1
        while i >= 0 and self.arr[i][x] != None:
            length += 1
            i -= 1
        i = y + 1
        while i <= 6 and self.arr[i][x] != None:
            length += 1
            i += 1
        if self.arr[y][x].unbroken == False and self.arr[y][x].cracked == False and length == self.arr[y][x].number:
            self.arr[y][x].remove()
            self.widget_count -= 1

            # check if adjacent widgets are unbroken and if so crack them
            self.check_adjacent(x, y)
            return True

        #pygame.time.wait(20)
        return False

    def check_adjacent(self, x, y):
        if x >= 1:
            widget = self.arr[y][x-1]
            if widget != None:
                widget.check_break()
        if x <= 5:
            widget = self.arr[y][x+1]
            if widget != None:
                widget.check_break()
        if y >= 1:
            widget = self.arr[y-1][x]
            if widget != None:
                widget.check_break()
        if y <= 5:
            widget = self.arr[y+1][x]
            if widget != None:
                widget.check_break()



    def drop(self, widget):
        if widget.active == 1:
            if self.arr[widget.loc_y][widget.loc_x] != None:
                return False

            # Drop until widget lands
            while widget.loc_y < 6 and self.arr[widget.loc_y + 1][widget.loc_x] == None:
                #self.clear()      # Erase where widget was
                widget.loc_y += 1         # Move down 1 spot
                #self.draw()       # Redraw screen


            self.arr[widget.loc_y][widget.loc_x] = widget    # Lock in the widget's position
            #self.clear()
            widget.active = 0     # Widget is now inactive
            #self.draw()       # Redraw screen

            return True



    def scoot(self):
        boardChanged = False
        for x in range(7):
            for y in reversed(range(6)):
                widget = self.arr[y][x]
                nextSpot = self.arr[y+1][x]
                yCopy = y

                while widget != None and nextSpot == None and yCopy <= 5:
                    
                    myWidget = self.arr[yCopy][x]
                    #myWidget.clear()

                    #pygame.time.wait(200)

                    myWidget.loc_y += 1
                    self.arr[yCopy + 1][x] = myWidget
                    self.arr[yCopy][x] = None
                    #myWidget.draw()
                    myWidget.redraw(prev_y=myWidget.loc_y-1)
                    boardChanged = True
                    
                    widget = self.arr[yCopy+1]
                    if yCopy+2 <= 6:
                        nextSpot = self.arr[yCopy+2][x]
                    yCopy += 1

                    

        if boardChanged:
            if config.use_gui:
                pygame.time.wait(100)
            self.scoot()
            return True
        else:
            return False
        #return boardChanged


    def clean(self):
        boardChanged = False
        for x in range(7):
            for y in range(7):
                if self.arr[y][x] != None and self.arr[y][x].delete == 1:
                    if config.combo_modifier > 0:
                        
                        logger.debug("Combo %d\n\tScore += %d", config.combo_modifier, config.combo_list[config.combo_modifier])

                    config.score += config.combo_list[config.combo_modifier]

                    boardChanged = True
                    self.arr[y][x].clear()
                    self.arr[y][x] = None
                    if config.use_gui:
                        pygame.time.wait(200)

        if boardChanged:
            config.combo_modifier += 1
        return boardChanged
    


    def check(self):
        boardChanged = False

        # Check each cell to see if the widget will be destroyed
        for x in range(7):
            for y in range(7):
                if self.check_cell(x, y) == True:
                    boardChanged = True

        if config.use_gui:
            pygame.time.wait(10)
        if self.clean() == True:
            boardChanged = True
        if config.use_gui:
            pygame.time.wait(10)
        if self.scoot() == True:
            boardChanged = True

        if boardChanged == True:
            self.check()

        if config.combo_modifier > config.longest_combo:
            config.longest_combo = config.combo_modifier
        config.combo_modifier = 0

            
    def add_unbroken_row(self):
        for x in range(7):
            for y in range(7):
                widget = self.arr[y][x]

                if widget is not None:
                    nextSpot = self.arr[y-1][x]
                    #widget.clear()
                    widget.loc_y -= 1
                    self.arr[y-1][x] = widget
                    self.arr[y][x] = None
                    #widget.draw()
                    widget.redraw(prev_y=widget.loc_y+1)

        for x in range(7):
            widget = Widget(True, x, 6)
            self.arr[6][x] = widget

        self.print_board()
        #pygame.display.flip()
        self.check()
        self.widget_count += 7


    def level_check(self):
        config.level_widgets_remaining -= 1

        # Finished level widgets, level up - add unbroken row
        if config.level_widgets_remaining == 0:
            config.level += 1
            config.score += 7000
            config.level_widgets_remaining = config.BASE_LEVEL_WIDGET_COUNT - config.level + 1
            if config.level_widgets_remaining < config.MINIMUM_LEVEL_WIDGET_COUNT:
                config.level_widgets_remaining += 1
            #self.check_game_over(row_add=True)
            self.check_game_over(row_add=True)
            self.add_unbroken_row()


    def check_game_over(self, row_add=False):
        if row_add:
            for x in range(7):
                if self.arr[0][x] is not None:
                    config.game_over = True
        
        elif not row_add:
            top_row_full = True
            for x in range(7):
                if self.arr[0][x] is None:
                    top_row_full = False

            if top_row_full:
                config.game_over = True

        if config.game_over:
            logger.info("Game Over!\nScore: %d\nLevel: %d\nLongest Combo: %d", config.score, config.level, config.longest_combo)




    def print_board(self):
        for row in self.arr:
            for val in row:
                if val is not None:
                    #logger.debug('{:4}'.format(val.number))
                    print '{:4}'.format(val.number),
                else:
                    #logger.debug('{:4}'.format(0))
                    print '{:4}'.format(0),
            print "\n"
# end Board class
