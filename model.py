import pygame
from eventmanager import *

from board import Board
from widget import Widget

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

        elif isinstance(event, LeftEvent):
            # move widget left
            self.active_widget.left()

        elif isinstance(event, RightEvent):
            # move widget right
            self.active_widget.right()

        elif isinstance(event, DownEvent):
            # drop widget
            self.board.drop(self.active_widget)

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

