#!/usr/bin/python2

from params import *
from util import *
import pygame

# various GUI constants
SKILLBOX_DIMS = (36, 36)
DASH_OFFSET   = (87, 2)
BLINK_OFFSET  = (125, 2)
SHOOT_OFFSET  = (163, 2)
SLOW_OFFSET   = (201, 2)
NAME_HEIGHT   = 10
NAME_YOFFSET  = 38

CD_COLOR      = (0,0,0,160)
SLOW_ON_COLOR = (0,200,200,100)

skillbarimg = pygame.image.load("img/skillbar.png").convert_alpha()

def draw_progress(screen, x, y, w, h, prog, color = CD_COLOR, overlay_name = True):
    '''draws a "clock" progress overlay over a square'''
    prog = 1-prog # I messed up

    # need to use an overlay for the alpha channel to work
    overlay = pygame.Surface((w, h + NAME_HEIGHT), pygame.SRCALPHA)

    def sq(t):
        '''Produces the point on the boundary of the square at progess t'''
        if t < 1.0/8:
            return [w/2 + 4*w*t , 0]
        elif t < 3.0/8:
            return [w-1 , - h/2 + 4*h*t]
        elif t < 5.0/8:
            return [5*w/2 - 4*w*t , h-1]
        elif t < 7.0/8:
            return [0, 7*h/2 - 4*h*t]
        else:
            return [-7*w/2 + 4*w*t, 0]

    points = [0, 1.0/8, 3.0/8, 5.0/8, 7.0/8, 1]
    for i in range(5):
        if prog > points[i]:
            triangle = [(w/2,h/2), sq(points[i]), sq(min(prog,points[i+1]))]
            print 'triangle is %s' % triangle
            pygame.draw.polygon(overlay, color, triangle)

    if overlay_name and prog > 0.0:
        pygame.draw.rect(overlay, color, [0, NAME_YOFFSET, w, NAME_HEIGHT])

    screen.blit(overlay, (x,y))

def draw_skillbar(screen, has_dash, blinkcd, shootcd, slow_charge, slow_on, dirty_rects):
    x0 = 0
    y0 = GAME_SIZE[1]

    screen.blit(skillbarimg, (x0, y0))
    draw_progress(screen, x0+DASH_OFFSET[0], y0+DASH_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], has_dash)
    draw_progress(screen, x0+BLINK_OFFSET[0], y0+BLINK_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], blinkcd)
    draw_progress(screen, x0+SHOOT_OFFSET[0], y0+SHOOT_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], shootcd)
    draw_progress(screen, x0+SLOW_OFFSET[0], y0+SLOW_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], slow_charge/SLOW_MAX_CHARGE, overlay_name=False)
    if slow_on:
        pygame.draw.rect(screen, SLOW_ON_COLOR, [x0+SLOW_OFFSET[0]-1, y0+SLOW_OFFSET[1]-1,
                                                 SKILLBOX_DIMS[0]+2, SKILLBOX_DIMS[1]+2], 1)

    # TODO: in the future, should actually find dirty rects intelligently
    dirty_rects.append(( x0, y0, skillbarimg.get_width(), skillbarimg.get_height() ))
