#!/usr/bin/env python2

import sys, pygame, time
import keys
from level import level, lvl_rects
from Ent import *
from params import *
from util import *
pygame.init()

bgcolor = 255, 255, 255

screen = pygame.display.set_mode(SCREEN_SIZE)

userimg = pygame.image.load("img/guy.png")
user = Ent(100, 350, userimg.get_width(), userimg.get_height(), userimg)

while 1:
    print "speed: %s,  posn: (%s,%s), grounded: %s" %\
        (user.speed, user.xpos, user.ypos, user.grounded)
    time.sleep(FRAME_LENGTH)
    pr = pygame.key.get_pressed()

    jumping = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == keys.JUMP and user.grounded:
                jumping = True
                sp[1] = -JUMP_SPEED
                user.grounded = False

    sp = user.speed
    if user.grounded:
        sp[0] = 0
        if pr[keys.LEFT]:
            sp[0] = -RUN_SPEED
        elif pr[keys.RIGHT]:
            sp[0] = RUN_SPEED
    else:
        # handle horizontal speed/acceleration
        sgn = sp[0] / abs(sp[0]) if sp[0] != 0 else 1
        if abs(sp[0]) > AIR_SPEED:
            print "\tSPEED DRAG"
            sp[0] -= sgn * FRIC_DECEL
        
        if pr[keys.LEFT] and sp[0] >= -AIR_SPEED:
            sp[0] = max(-AIR_SPEED, sp[0] - AIR_ACCEL)
        elif pr[keys.RIGHT] and sp[0] <= AIR_SPEED:
            sp[0] = min(AIR_SPEED, sp[0] + AIR_ACCEL)
        elif abs(sp[0]) < FRIC_DECEL:
            print "\tDRAG STOP"
            sp[0] = 0
        else:
            print "\tDRAG"
            sp[0] -= sgn*FRIC_DECEL

        # handle vertical speed/acceleration
        # TODO: terminal velocity?
        sp[1] += GRAV_ACCEL

    # update position with speed; check collisions
    oldpos = oldx, oldy = user.xpos, user.ypos
    user.xpos += sp[0]
    user.ypos += sp[1]

    if sp[0] <= 0 and sp[1] >= 0:
        front = oldx, oldy + user.height
    elif sp[0] >= 0 and sp[1] >= 0:
        front = oldx + user.width, oldy + user.height
    elif sp[0] >= 0 and sp[1] <= 0:
        front = oldx + user.width, oldy
    elif sp[0] <= 0 and sp[1] <= 0:
        front = oldpos

    #collisions = user.get_rect().collidelistall(lvl_rects)
    collisions = [r for r in lvl_rects\
                    if rect_coll(user.get_rect(), r, COLL_DIST)]
    if collisions:
        minhoriz, minvert = float('inf'), float('inf')
        for rect in collisions:
            wx1, wx2, wy1, wy2 = rect[0]-COLL_SEP, rect[0]+rect[1]+COLL_SEP,\
                                 rect[1]-COLL_SEP, rect[1]+rect[3]+COLL_SEP
            minhoriz = min(minhoriz, cast(front, sp, ((wx1,wy1), (wx1,wy2))),\
                                     cast(front, sp, ((wx2,wy1), (wx2,wy2))),)
            minvert  = min(minvert,  cast(front, sp, ((wx1,wy1), (wx2,wy1))),\
                                     cast(front, sp, ((wx1,wy2), (wx2,wy2))),)
        t = min(minhoriz, minvert)
        user.xpos = oldpos[0] + t*sp[0]
        user.ypos = oldpos[1] + t*sp[1]
        if t == float('inf'):
            sys.exit()
        if minhoriz < minvert:
            sp[0] = 0
        else:
            if sp[1] > 0:
                user.grounded = True
            sp[1] = 0

    # TODO: don't flip every frame
    screen.fill(bgcolor)
    user.blitto(screen)
    pygame.display.flip()
