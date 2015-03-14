"""
File: widget.py
Author: Dillon Beck

Classes:
    Widget: Manages widget attributes.

"""
import logging
import pygame
from random import randint

import config


LOGGER = logging.getLogger(__name__)

class Widget(object):
    """Widget class that manages breaking/cracking widgets and movement.

    #TODO: loc_x and loc_y -> (loc_X, loc_y) or (row, column)
    #TODO: unbroken/cracked -> one int attribute? 
    #TODO: sprite should be here?

    Attribute:
        number: Int representing the number of the widget.
        unbroken: Boolean indicating whether widget is unbroken.
        cracked: Boolean indicating whether widget is cracked.
        sprite: Sprite for the widget.
        loc_x: Row the widget occupies.
        loc_y: Column the widget occupies.
        active: Whether the widget is the one being moved by the user.
        delete: Whether the widget is deleted or not.

    """

    def __init__(self, unbroken=False, row=0, column=0):
        self.number = randint(1, 7)
        if unbroken or (randint(1, 8) == 8):
            self.unbroken = True
            self.cracked = False
            if config.use_gui:
                self.sprite = config.icon_arr[7]
        else:
            self.unbroken = False
            self.cracked = False
            if config.use_gui:
                self.sprite = config.icon_arr[self.number - 1]

        if unbroken:
            self.loc_x = row
            self.loc_y = column
            self.active = 0
        else:
            self.loc_x = config.DROP_X
            self.loc_y = config.DROP_Y
            self.active = 1

        self.delete = 0
        self.draw()


    def clear(self):
        """Remove the widget from the screen.

        #TODO: This is gui stuff...

        """

        if config.use_gui:
            config.gui.clear_widget(self.active, self.loc_x, self.loc_y)

            pygame.display.flip()


    def draw(self):
        """Draw the widget on the screen.

        #TODO: This is gui stuff..

        """


        if config.use_gui:
            config.gui.draw_widget(self.sprite, self.active, self.loc_x, self.loc_y)

            pygame.display.flip()


    def redraw(self, prev_x=None, prev_y=None, prev_active=None):
        """Redraw the widget on the board.

        #TODO: This is all gui stuff... should it be here?

        Args:
            prev_x: The x location where the widget just was.  This is where the
                sprite for the widget is currently drawn on the screen before
                being updated here.  If None, the widget's last and current x
                position are the same.
            prev_y: The y location where the widget just was.  This is where the
                sprite for the widget is currently drawn on the screen before
                being updated here.  If None, the widget's last and current y
                position are the same.
            prev_active: Int indicating the widget's previous active state.
            #TODO: Should self.active be an into 1 or 0, or a bool?

        """

        if prev_x is None:
            prev_x = self.loc_x
        if prev_y is None:
            prev_y = self.loc_y
        if prev_active is None:
            prev_active = self.active

        if config.use_gui:
            config.gui.clear_widget(prev_active, prev_x, prev_y)
            config.gui.draw_widget(self.sprite, self.active, self.loc_x, self.loc_y)


    def right(self):
        """Move the widget right 1 spot.

        The widget will move right 1 spot, but its x location will not be 
        greater than 7.

        """

        if self.loc_x < 6 and self.active == 1:
            self.loc_x += 1

            self.redraw(prev_x=self.loc_x-1)


    def left(self):
        """Move the widget left 1 spot.

        The widget will move left 1 spot, but its x location will not be less
        than 0.

        """

        if self.loc_x >= 1 and self.active == 1:
            self.loc_x -= 1

            self.redraw(prev_x=self.loc_x+1)
    

    # Mark a cell to be deleted
    def remove(self):
        """Mark a widget as deleted.
        #TODO: Should this even be a method?
        #TODO: Should/can this be renamed to delete?
        """

        self.delete = 1

        if config.use_gui:
            self.clear()
            pygame.time.wait(100)


    def check_break(self):
        """Break or crack the widget.

        Check if the widget is unbroken or cracked.  If unbroken, crack the 
        widget.  If cracked, break the widget.  If broken, do nothing.
        Updates the widget's sprite.
        #TODO: shouldn't have any stuff to do with the sprite?

        """

        new_sprite = None

        if  self.cracked == True:
            self.cracked = False
            if config.use_gui:
                new_sprite = config.icon_arr[self.number - 1]
            #self.sprite = config.icon_arr[self.number - 1]
            #self.draw()
        if self.unbroken == True:
            self.unbroken = False
            self.cracked = True
            if config.use_gui:
                new_sprite = config.icon_arr[8]
            #self.sprite = config.icon_arr[8]
            #self.draw()

        if config.use_gui:
            if new_sprite is not None:
                self.sprite = new_sprite
                self.draw()
