#!/usr/bin/env python2

import sys, pygame, time
import keys
from level import level
from Ent import *
from params import *
from util import *
from collision import coll_move
pygame.init()

bgcolor = 255, 255, 255

screen = pygame.display.set_mode(SCREEN_SIZE)

userimg = pygame.image.load("img/guy.png")
blockimg = pygame.image.load("img/block.png")
user = Ent(SPAWN[0], SPAWN[1], userimg.get_width(), userimg.get_height(), userimg)

frame = -1 # frame counter
while 1:
    frame += 1
    time.sleep(FRAME_LENGTH)
    t0 = int(round(time.time() * 1000))
    pr = pygame.key.get_pressed()

    # check if user has fallen off platform
    if user.grounded and (user.right() < user.grounded.left() or\
                          user.left() > user.grounded.right()):
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

            if event.unicode == '+':
                FRAME_LENGTH /= 2.0
            elif event.unicode == '-':
                FRAME_LENGTH *= 2.0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = event.pos
            new = Ent(mx, my, blockimg.get_width(), blockimg.get_height(), blockimg)
            level.append(new)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dirn = vsub(event.pos, user.centre())
            user.speed = vscale(BOOST_SPEED/vnorm(dirn), dirn)

    sp = user.speed
    if user.grounded:
        sp[0] = user.grounded.speed[0]
        sp[1] = user.grounded.speed[1]
        if pr[keys.LEFT]:
            sp[0] -= RUN_SPEED
        elif pr[keys.RIGHT]:
            sp[0] += RUN_SPEED
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

    # update platform speeds
    for item in level:
        if item.behaviour:
            item.behaviour(item, frame)
    
    print "\nspeed: %s,  posn: (%s,%s), grounded: %s" %\
        (user.speed, user.xpos, user.ypos, user.grounded)
    print "plat: %s" % level[1]
    coll_move(user, level)

    # TODO: don't flip every frame
    screen.fill(bgcolor)
    user.blitto(screen)
    for item in level:
        item.blitto(screen)
    pygame.display.flip()
    render_time = int(round(time.time() * 1000)) - t0
    #print "render time: %s" % render_time
