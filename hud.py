#!/usr/bin/python2

from params import *
import pygame

skillbarimg = pygame.image.load("img/skillbar.png").convert_alpha()

def draw_skillbar(screen, dirty_rects):
    screen.blit(skillbarimg, (0, GAME_SIZE[1]))

    # TODO: in the future, should actually find dirty rects intelligently
    dirty_rects.append(( 0, GAME_SIZE[1], skillbarimg.get_width(), skillbarimg.get_height() ))
