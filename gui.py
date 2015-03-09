import logging

import pygame

import config


logger = logging.getLogger(__name__)

class Gui():
    def __init__(self):
        i = 0

    @staticmethod
    def setup():
        pygame.display.set_caption('Drop7')


    @staticmethod
    def printGameInfo(score, level, remaining_widgets):
        Gui.printScore(score)
        Gui.printLevel(level)
        Gui.printRemainingWidgets(remaining_widgets)


    @staticmethod
    def printScore(score):
        text = config.font.render("Score: " + str(score), 1, config.WHITE)
        textpos = text.get_rect(left=0)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)


    @staticmethod
    def printLevel(level):
        text = config.font.render("Level: " + str(level), 1, config.WHITE)
        textpos = text.get_rect(top=12)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)


    @staticmethod
    def printRemainingWidgets(remaining_widgets):
        text = config.font.render("Remaining Widgets: " + str(remaining_widgets), 1, config.WHITE)
        textpos = text.get_rect(top=24)
        pygame.draw.rect(config.screen, config.BLACK, textpos)
        config.screen.blit(text, textpos)


    @staticmethod
    def clear_widget(active_widget, loc_x, loc_y):
        if active_widget:
            y = loc_y+1
        else:
            y = loc_y+2

        # if active_widget:
        #     box = pygame.Rect(loc_x * config.WIDGET_WIDTH, (loc_y+1) * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)

        # else:
        #     box = pygame.Rect(loc_x * config.WIDGET_WIDTH, (loc_y+2) * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)
        
        box = pygame.Rect(loc_x * config.WIDGET_WIDTH, y * config.WIDGET_HEIGHT, config.WIDGET_WIDTH-1, config.WIDGET_HEIGHT-1)
        pygame.draw.rect(config.screen, config.BLACK, box, 0)



    @staticmethod
    def draw_widget(sprite, active_widget, loc_x, loc_y):
        if active_widget:
            config.screen.blit(sprite, (loc_x * config.WIDGET_WIDTH, (loc_y+1) * config.WIDGET_HEIGHT))
        else:
            config.screen.blit(sprite, (loc_x * config.WIDGET_WIDTH, (loc_y+2) * config.WIDGET_HEIGHT))



