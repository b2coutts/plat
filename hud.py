#!/usr/bin/python2

from params import *
from util import *
import pygame

# various GUI constants
SKILLBOX_DIMS = (36, 36)
DASH_OFFSET   = (87, 2)
BLINK_OFFSET  = (125, 2)
SHOOT_OFFSET  = (163, 2)

skillbarimg = pygame.image.load("img/skillbar.png").convert_alpha()

def draw_progress(screen, x, y, w, h, prog, color = (30,30,30,80)):
    '''draws a "clock" progress overlay over a square'''
    prog = 1-prog # I messed up
    centre = x + w/2, y + h/2

    def sq(t):
        '''Produces the point on the boundary of the square at progess t'''
        if t < 1.0/8:
            return [x + w/2 + 4*w*t , y]
        elif t < 3.0/8:
            return [x+w-1 , y - h/2 + 4*h*t]
        elif t < 5.0/8:
            return [x + 5*w/2 - 4*w*t , y+h-1]
        elif t < 7.0/8:
            return [x, y + 7*h/2 - 4*h*t]
        else:
            return [x - 7*w/2 + 4*w*t, y]

    points = [0, 1.0/8, 3.0/8, 5.0/8, 7.0/8, 1]
    for i in range(5):
        if prog > points[i]:
            triangle = [centre, sq(points[i]), sq(min(prog,points[i+1]))]
            print 'triangle is %s' % triangle
            pygame.draw.polygon(screen, color, triangle)

def draw_skillbar(screen, blinkcd, shootcd, dirty_rects):
    x0 = 0
    y0 = GAME_SIZE[1]

    screen.blit(skillbarimg, (x0, y0))
    draw_progress(screen, x0+BLINK_OFFSET[0], y0+BLINK_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], blinkcd)
    draw_progress(screen, x0+SHOOT_OFFSET[0], y0+SHOOT_OFFSET[1], SKILLBOX_DIMS[0],\
                  SKILLBOX_DIMS[1], shootcd)

    # TODO: in the future, should actually find dirty rects intelligently
    dirty_rects.append(( x0, y0, skillbarimg.get_width(), skillbarimg.get_height() ))
