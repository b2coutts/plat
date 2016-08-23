#!/usr/bin/env python2

import sys, pygame, time
import keys
from level import level, lvl_rects
from Ent import *
from params import *
from util import *
from collision import coll_move
pygame.init()

bgcolor = 255, 255, 255

screen = pygame.display.set_mode(SCREEN_SIZE)

userimg = pygame.image.load("img/guy.png")
blockimg = pygame.image.load("img/block.png")
user = Ent(100, 350, userimg.get_width(), userimg.get_height(), userimg)

while 1:
    print "speed: %s,  posn: (%s,%s), grounded: %s" %\
        (user.speed, user.xpos, user.ypos, user.grounded)
    time.sleep(FRAME_LENGTH)
    pr = pygame.key.get_pressed()

    # check if user has fallen off platform
    if user.grounded and (user.xpos+user.width < user.grounded[0] or
                          user.xpos > user.grounded[0]+user.grounded[2]):
        user.grounded = False

    jumping = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == keys.JUMP and user.grounded:
                jumping = True
                sp[1] = -JUMP_SPEED
                user.grounded = False

            # debug stuff
            if event.key == pygame.K_p:
                print "levels: %s" % lvl_rects
            elif event.unicode == '+':
                FRAME_LENGTH /= 2.0
            elif event.unicode == '-':
                FRAME_LENGTH *= 2.0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            new = Ent(mx, my, blockimg.get_width(), blockimg.get_height(), blockimg)
            level.append(new)
            lvl_rects.append(new.get_rect())

    sp = user.speed
    if user.grounded:
        sp[0] = sp[1] = 0
        if pr[keys.LEFT]:
            sp[0] = -RUN_SPEED
        elif pr[keys.RIGHT]:
            sp[0] = RUN_SPEED
    else:
        # handle horizontal speed/acceleration
        sgn = sp[0] / abs(sp[0]) if sp[0] != 0 else 1
        fdecel = FRIC_DECEL_SLOW if abs(sp[0] <= FRIC_DECEL_SLOW_THRES)\
                                 else FRIC_DECEL
        if abs(sp[0]) > AIR_SPEED:
            sp[0] -= sgn * fdecel
        
        if pr[keys.LEFT] and sp[0] >= -AIR_SPEED:
            sp[0] = max(-AIR_SPEED, sp[0] - AIR_ACCEL)
        elif pr[keys.RIGHT] and sp[0] <= AIR_SPEED:
            sp[0] = min(AIR_SPEED, sp[0] + AIR_ACCEL)
        elif abs(sp[0]) < fdecel:
            sp[0] = 0
        else:
            sp[0] -= sgn*fdecel

        # handle vertical speed/acceleration
        # TODO: terminal velocity?
        sp[1] += GRAV_ACCEL

    coll_move(user, lvl_rects)

    # TODO: don't flip every frame
    screen.fill(bgcolor)
    user.blitto(screen)
    for item in level:
        item.blitto(screen)
    pygame.display.flip()
