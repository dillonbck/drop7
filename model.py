import pygame
from eventmanager import *

from board import Board
from widget import Widget
import config

class GameEngine(object):
    """
    Tracks the game state.
    """

    def __init__(self, evManager):
        """
        evManager (EventManager): Allows posting messages to the event queue.

        Attributes:
        running (bool): True while the engine is online. Changed via QuitEvent().
        """

        self.evManager = evManager
        evManager.RegisterListener(self)
        self.running = False

        self.board = Board()
        self.active_widget = Widget()

    def notify(self, event):
        """
        Called by an event in the message queue. 
        """

        if isinstance(event, QuitEvent):
            self.running = False


        elif isinstance(event, MoveEvent):
            move_event = WidgetMoveEvent()
            move_event.prev_x = self.active_widget.loc_x
            move_event.prev_active = self.active_widget.active

            if event.direction == MoveEvent.DIR_LEFT:
                self.active_widget.left()
            elif event.direction == MoveEvent.DIR_RIGHT:
                self.active_widget.right()
            elif event.direction == MoveEvent.DIR_DOWN:
                pass

            move_event.cur_x = self.active_widget.loc_x
            move_event.prev_y = config.DROP_Y
            move_event.cur_y = config.DROP_Y
            move_event.cur_active = self.active_widget.active
            if config.use_gui:
                move_event.sprite = self.active_widget.sprite

            self.evManager.Post(move_event)



    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify(). 
        """
        self.running = True
        self.evManager.Post(InitializeEvent())
        while self.running:
            newTick = TickEvent()
            self.evManager.Post(newTick)

