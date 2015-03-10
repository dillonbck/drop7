"""
The docstring for a module should generally list the classes, exceptions and 
functions (and any other objects) that are exported by the module, with a 
one-line summary of each. (These summaries generally give less detail than the 
summary line in the object's docstring.)
"""
import logging
import pygame

import config

from widget import Widget


LOGGER = logging.getLogger(__name__)

class Board(object):
    """Summary of class here.

    Longer class info...
    Longer class info...

    Attribute:
        attribute: A boolean attribute explanation.
    """


    def __init__(self):

        self.arr = [[None for x in range(7)] for y in range(7)]

        self.widget_count = 0

    # Check to see if the widget at the specified location will be destroyed
    def check_cell(self, x_loc, y_loc):
        """Check if the widget at specified location will be destroyed.

        Check if the widget at the specified location is subject to destruction:
            widget's number == number of widgets currently in the row or column.


        Args:
            argument: Explanation.
            x_loc: X (column) location of widget to check.
            y_loc: Y (row) location of widget to check.

        Returns:
            Returns a boolean indicating whether the widget at the specified 
            location will be destroyed.

        """

        # If cell empty, return False
        if self.arr[y_loc][x_loc] == None:
            return False

        # Check horizontal widget removals
        length = 1
        i = x_loc - 1
        while i >= 0 and self.arr[y_loc][i] != None:
            length += 1
            i -= 1
        i = x_loc + 1
        while i <= 6 and self.arr[y_loc][i] != None:
            length += 1
            i += 1
        if (self.arr[y_loc][x_loc].unbroken == False and self.arr[y_loc][x_loc].cracked == False
                and length == self.arr[y_loc][x_loc].number):   

            self.arr[y_loc][x_loc].remove()  # Destroy this widget
            self.widget_count -= 1

            # check if adjacent widgets are unbroken and if so crack them
            self.check_adjacent(x_loc, y_loc)
            return True

        # Check vertical widget removals
        i = y_loc - 1
        length = 1
        while i >= 0 and self.arr[i][x_loc] != None:
            length += 1
            i -= 1
        i = y_loc + 1
        while i <= 6 and self.arr[i][x_loc] != None:
            length += 1
            i += 1
        if (self.arr[y_loc][x_loc].unbroken == False and self.arr[y_loc][x_loc].cracked == False
                and length == self.arr[y_loc][x_loc].number):
            self.arr[y_loc][x_loc].remove()
            self.widget_count -= 1

            # check if adjacent widgets are unbroken and if so crack them
            self.check_adjacent(x_loc, y_loc)
            return True

        #pygame.time.wait(20)
        return False

    def check_adjacent(self, x_loc, y_loc):
        """Check if widgets adjacent to specified location will break or crack. 

        For each location adjacent to the specified location, check if there is
        a widget, and if so, check if it will break or crack.
        Will crack any unbroken widgets adjacent to specified location.
        Will break any cracked widgets adjacent to specified location.

        Args:
            x_loc: X (column) location to check adjacent.
            y_loc: Y (row) location to check adjacent. 

        Returns:
            Returns nothing.

        """

        if x_loc >= 1:
            widget = self.arr[y_loc][x_loc-1]
            if widget != None:
                widget.check_break()
        if x_loc <= 5:
            widget = self.arr[y_loc][x_loc+1]
            if widget != None:
                widget.check_break()
        if y_loc >= 1:
            widget = self.arr[y_loc-1][x_loc]
            if widget != None:
                widget.check_break()
        if y_loc <= 5:
            widget = self.arr[y_loc+1][x_loc]
            if widget != None:
                widget.check_break()



    def drop(self, widget):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        if widget.active == 1:
            if self.arr[widget.loc_y][widget.loc_x] != None:
                return False

            # Drop until widget lands
            while widget.loc_y < 6 and self.arr[widget.loc_y + 1][widget.loc_x] == None:
                #self.clear()      # Erase where widget was
                widget.loc_y += 1         # Move down 1 spot
                #self.draw()       # Redraw screen

                widget.redraw(prev_y=widget.loc_y-1)

                if config.use_gui:  
                    pygame.time.wait(100)   

            self.arr[widget.loc_y][widget.loc_x] = widget    # Lock in the widget's position
            #self.clear()
            prev_active = widget.active
            widget.active = 0     # Widget is now inactive
            #self.draw()       # Redraw screen
            widget.redraw(prev_active=prev_active)

            if config.use_gui:
                pygame.time.wait(10)   
            return True



    def scoot(self):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        board_changed = False
        for x in range(7):
            for y in reversed(range(6)):
                widget = self.arr[y][x]
                next_spot = self.arr[y+1][x]
                y_copy = y

                while widget != None and next_spot == None and y_copy <= 5:
                    
                    my_widget = self.arr[y_copy][x]
                    #my_widget.clear()

                    #pygame.time.wait(200)

                    my_widget.loc_y += 1
                    self.arr[y_copy + 1][x] = my_widget 
                    self.arr[y_copy][x] = None
                    #my_widget.draw()
                    my_widget.redraw(prev_y=my_widget.loc_y-1)
                    board_changed = True
                    
                    widget = self.arr[y_copy+1]
                    if y_copy+2 <= 6:
                        next_spot = self.arr[y_copy+2][x]
                    y_copy += 1

                    

        if board_changed:
            if config.use_gui:
                pygame.time.wait(100)
            self.scoot()
            return True
        else:
            return False
        #returnboard_changed 


    def clean(self):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        board_changed = False
        for x in range(7):
            for y in range(7):
                if self.arr[y][x] != None and self.arr[y][x].delete == 1:
                    if config.combo_modifier > 0:
                        
                        LOGGER.debug("Combo %d\n\tScore += %d", 
                                     config.combo_modifier, 
                                     config.combo_list[config.combo_modifier])

                    config.score += config.combo_list[config.combo_modifier]

                    board_changed = True
                    self.arr[y][x].clear()
                    self.arr[y][x] = None
                    if config.use_gui:
                        pygame.time.wait(200)

        if board_changed:
            config.combo_modifier += 1
        return board_changed 
    


    def check(self):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        board_changed = False

        # Check each cell to see if the widget will be destroyed
        for x in range(7):
            for y in range(7):
                if self.check_cell(x, y) == True:
                    board_changed = True

        if config.use_gui:
            pygame.time.wait(10)
        if self.clean() == True:
            board_changed = True
        if config.use_gui:
            pygame.time.wait(10)
        if self.scoot() == True:
            board_changed = True

        if board_changed == True:
            self.check()

        if config.combo_modifier > config.longest_combo:
            config.longest_combo = config.combo_modifier
        config.combo_modifier = 0

            
    def add_unbroken_row(self):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        for x in range(7):
            for y in range(7):
                widget = self.arr[y][x]

                if widget is not None:
                    next_spot = self.arr[y-1][x]
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
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

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
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

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
            LOGGER.info("Game Over!\nScore: %d\nLevel: %d\nLongest Combo: %d", 
                        config.score, config.level, config.longest_combo)




    def print_board(self):
        """One line summary.

        Extended method summary.

        Args:
            argument: Explanation.

        Returns:
            Explanation.
            Example:

        Raises:
            Errorname: Explanation

        """

        for row in self.arr:
            for val in row:
                if val is not None:
                    LOGGER.debug('{:4}'.format(val.number))
                    #print '{:4}'.format(val.number),
                else:
                    LOGGER.debug('{:4}'.format(0))
                    #print '{:4}'.format(0),
# end Board class
