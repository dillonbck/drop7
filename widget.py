import logging
import pygame
from random import randint
import config
from eventmanager import *


logger = logging.getLogger(__name__)

class Widget:

    UNBROKEN = 2
    CRACKED = 1
    BROKEN = 0

    def __init__(self, game_engine, unbroken=False, x=0, y=0):
        self.game_engine = game_engine

        self.number = randint(1,7)
        #self.number = 2
        if unbroken or (randint(1,8) == 8):    # mostly broken
            self.state = Widget.UNBROKEN

            if config.use_gui:
                self.sprite = config.icon_arr[7]
            #self.number = 4
        else:
            self.state = Widget.BROKEN
            
            if config.use_gui:
                self.sprite = config.icon_arr[self.number - 1]
            #color = self.sprite.get_at((0,0))
            #self.sprite.set_colorkey(color)

        if unbroken:
            self.loc_x = x
            self.loc_y = y
            self.active = 0
        else:
            self.loc_x = self.game_engine.DROP_X
            self.loc_y = self.game_engine.DROP_Y
            self.active = 1

        self.delete = 0
        self.draw()

        ev = WidgetCreateEvent()
        ev.active_widget = self.active
        ev.loc_x = self.loc_x
        ev.loc_y = self.loc_y
        ev.state = self.state
        ev.number = self.number 

        self.game_engine.evManager.Post(ev)

    def clear(self):
        # if self.active:
        #     box = pygame.Rect(self.loc_x * config.WIDGET_WIDTH, (self.loc_y+1) * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)

        # else:
        #     box = pygame.Rect(self.loc_x * config.WIDGET_WIDTH, (self.loc_y+2) * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)
        # pygame.draw.rect(config.BLACK, box, 0)
        # #pygame.draw.rect(WHITE)

        if config.use_gui:
            config.gui.clear_widget(self.active, self.loc_x, self.loc_y)

            pygame.display.flip()


        ev = WidgetClearEvent()
        ev.active_widget = self.active
        ev.loc_x = self.loc_x
        ev.loc_y = self.loc_y

        self.game_engine.evManager.Post(ev)

    def draw(self):
        # if self.active:
        #     screen.blit(self.sprite, (self.loc_x * config.WIDGET_WIDTH, (self.loc_y+1) * config.WIDGET_HEIGHT))
        # else:
        #     screen.blit(self.sprite, (self.loc_x * config.WIDGET_WIDTH, (self.loc_y+2) * config.WIDGET_HEIGHT))

        if config.use_gui:
            config.gui.draw_widget(self.sprite, self.active, self.loc_x, self.loc_y)

            pygame.display.flip()


    def right(self):
        if self.loc_x < 6 and self.active == 1:

            #self.clear()
            self.loc_x += 1
            #self.draw()

            # self.redraw(prev_x=self.loc_x-1)

    def left(self):
        if self.loc_x >= 1 and self.active == 1:
            #self.clear()
            self.loc_x -= 1
            #self.draw()

            # self.redraw(prev_x=self.loc_x+1)
    

    # Mark a cell to be deleted
    def remove(self):
        self.delete = 1

        if config.use_gui:
            self.clear()
            pygame.time.wait(100)


    # def check_break(self):
    #     new_sprite = None

    #     if  self.cracked == True:
    #         self.cracked = False
    #         if config.use_gui:
    #             new_sprite = config.icon_arr[self.number - 1]
    #         #self.sprite = config.icon_arr[self.number - 1]
    #         #self.draw()
    #     if self.unbroken == True:
    #         self.unbroken = False
    #         self.cracked = True
    #         if config.use_gui:
    #             new_sprite = config.icon_arr[8]
    #         #self.sprite = config.icon_arr[8]
    #         #self.draw()

    #     if config.use_gui:
    #         if new_sprite is not None:
    #             self.sprite = new_sprite
    #             self.draw()


    def check_break(self):

        changed = False

        if self.state == Widget.CRACKED:
            self.state = Widget.BROKEN
            changed = True

        if self.state == Widget.UNBROKEN:
            self.state = Widget.CRACKED
            changed = True


        if changed:
            move_event = WidgetMoveEvent()
            move_event.prev_x = self.loc_x
            move_event.cur_x = self.loc_x
            move_event.prev_y = self.loc_y
            move_event.cur_y = self.loc_y
            move_event.prev_active = self.active
            move_event.cur_active = self.active
            move_event.state = self.state
            move_event.number = self.number

            self.game_engine.evManager.Post(move_event)

        # if  self.cracked == True:
        #     self.cracked = False

        # if self.unbroken == True:
        #     self.unbroken = False
        #     self.cracked = True
