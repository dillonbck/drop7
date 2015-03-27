import logging
import pygame
from eventmanager import *


from widget import Widget


logger = logging.getLogger(__name__)

class Board:

    def __init__(self, game_engine):

        self.arr = [[None for x in range(7)] for y in range(7)]

        self.widget_count = 0

        self.game_engine = game_engine

    # Check to see if the widget at the specified location will be destroyed
    def check_cell(self, x, y):
        if self.arr[y][x] is not None and self.arr[y][x].state == Widget.BROKEN:
            logger.debug("\nnumber: %d", self.arr[y][x].number)

            # If cell empty, return False
            if self.arr[y][x] == None:
                logger.debug("check_cell empty cell")
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

            logger.debug("horizontal check:")
            logger.debug("length == number?: %d == %d: %d", length, self.arr[y][x].number, length == self.arr[y][x].number)
            #if self.arr[y][x].unbroken == False and self.arr[y][x].cracked == False and length == self.arr[y][x].number:
            #if self.arr[y][x].state == Widget.BROKEN and length == self.arr[y][x].number:
            if length == self.arr[y][x].number:
                self.arr[y][x].remove()  # Destroy this widget
                self.widget_count -= 1

                # check if adjacent widgets are unbroken and if so crack them
                self.check_adjacent(x, y)
                pygame.time.wait(1000)
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
            logger.debug("vertical check:")
            logger.debug("length == number?: %d == %d: %d", length, self.arr[y][x].number, length == self.arr[y][x].number)
            #if self.arr[y][x].unbroken == False and self.arr[y][x].cracked == False and length == self.arr[y][x].number:
            #if self.arr[y][x].state == Widget.BROKEN and length == self.arr[y][x].number:
            if length == self.arr[y][x].number:
                self.arr[y][x].remove()
                self.widget_count -= 1

                # check if adjacent widgets are unbroken and if so crack them
                self.check_adjacent(x, y)
                pygame.time.wait(1000)
                return True

            pygame.time.wait(2000)
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

                    #myWidget.redraw(prev_y=myWidget.loc_y-1)

                    move_event = WidgetMoveEvent()
                    move_event.prev_x = x
                    move_event.cur_x = x
                    move_event.prev_y = yCopy
                    move_event.cur_y = yCopy + 1
                    move_event.prev_active = myWidget.active
                    move_event.cur_active = myWidget.active
                    move_event.state = myWidget.state
                    move_event.number = myWidget.number

                    self.game_engine.evManager.Post(move_event)


                    boardChanged = True
                    
                    widget = self.arr[yCopy+1]
                    if yCopy+2 <= 6:
                        nextSpot = self.arr[yCopy+2][x]
                    yCopy += 1

                    

        if boardChanged:
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
                    if self.game_engine.combo_modifier > 0:
                        
                        logger.debug("Combo %d\n\tScore += %d", self.game_engine.combo_modifier, self.game_engine.COMBO_LIST[self.game_engine.combo_modifier])

                    self.game_engine.score += self.game_engine.COMBO_LIST[self.game_engine.combo_modifier]

                    boardChanged = True
                    self.arr[y][x].clear()
                    self.arr[y][x] = None

        if boardChanged:
            self.game_engine.combo_modifier += 1
        return boardChanged
    


    def check(self):
        boardChanged = False

        # Check each cell to see if the widget will be destroyed
        for x in range(7):
            for y in range(7):
                if self.check_cell(x, y) == True:
                    boardChanged = True

        if boardChanged:
            self.clean()
            self.scoot()
            self.check()

        if self.game_engine.combo_modifier > self.game_engine.longest_combo:
            self.game_engine.longest_combo = self.game_engine.combo_modifier
        self.game_engine.combo_modifier = 0

            
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

                    #widget.redraw(prev_y=widget.loc_y+1)

                    move_event = WidgetMoveEvent()
                    move_event.prev_x = x
                    move_event.cur_x = x
                    move_event.prev_y = y
                    move_event.cur_y = y - 1
                    move_event.prev_active = widget.active
                    move_event.cur_active = widget.active
                    move_event.state = widget.state
                    move_event.number = widget.number

                    self.game_engine.evManager.Post(move_event)

        for x in range(7):
            widget = Widget(self.game_engine, True, x, 6)
            self.arr[6][x] = widget

        self.print_board()
        #pygame.display.flip()
        self.check()
        self.widget_count += 7

    def level_check(self):
        #config.level_widgets_remaining -= 1
        self.game_engine.level_widgets_remaining -= 1

        # Finished level widgets, level up - add unbroken row
        #if config.level_widgets_remaining == 0:
        if self.game_engine.level_widgets_remaining == 0:
            self.game_engine.level += 1
            self.game_engine.score += 7000
            self.game_engine.level_widgets_remaining = self.game_engine.BASE_LEVEL_WIDGET_COUNT - self.game_engine.level + 1

            #config.level += 1
            #config.score += 7000
            #config.level_widgets_remaining = self.game_engine.BASE_LEVEL_WIDGET_COUNT - config.level + 1
            if self.game_engine.level_widgets_remaining < self.game_engine.MINIMUM_LEVEL_WIDGET_COUNT:
                self.game_engine.level_widgets_remaining += 1
            #self.check_game_over(row_add=True)
            self.check_game_over(row_add=True)
            self.add_unbroken_row()


    def check_game_over(self, row_add=False):
        if row_add:
            for x in range(7):
                if self.arr[0][x] is not None:
                    self.game_engine.game_over = True
                    self.game_engine.running = False
        
        elif not row_add:
            top_row_full = True
            for x in range(7):
                if self.arr[0][x] is None:
                    top_row_full = False

            if top_row_full:
                self.game_engine.game_over = True
                self.game_engine.running = False

        if self.game_engine.game_over:
            logger.info("Game Over!\nScore: %d\nLevel: %d\nLongest Combo: %d", self.game_engine.score, self.game_engine.level, self.game_engine.longest_combo)




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
