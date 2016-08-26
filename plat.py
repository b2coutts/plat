#!/usr/bin/env python2

import sys, pygame, time
from params import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

import keys, audio
from lvl1 import level
from Ent import *
from util import *
from collision import coll_move

audio.bgm.play(loops=-1)

bgcolor = 255, 255, 255

userimg = pygame.image.load("img/lilguy.png").convert_alpha()
blockimg = pygame.image.load("img/block.png").convert()
user = Ent(level.spawn[0], level.spawn[1], userimg.get_width(),\
           userimg.get_height(), userimg)
user.level = level

def can_ground(usr, obst):
    return usr.right() >= obst.left() and\
           usr.left() <= obst.right() and\
           float_eq(usr.bottom(), obst.top())

frame = -1 # frame counter
avg_render_time = 0
avg_frame_time = 0
while 1:
    print ''
    frame += 1
    t0 = time.time()

    # check if user has fallen off platform
    if user.grounded and not can_ground(user, user.grounded):
        user.grounded = False
        for obst in level.obsts:
            if can_ground(user, obst):
                user.grounded = obst
                break

    # update platform speeds
    level.tick(frame, user)
    for obst in level.obsts:
        if obst.behaviour:
            obst.behaviour(obst, level, user, frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print 'avg render/frame: %sms,  %sms' % (avg_render_time*1000, avg_frame_time*1000)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == keys.JUMP and user.grounded:
                user.grounded = False
                user.jumping = 1

            # debug stuff
            if event.unicode == '+':
                FRAME_LENGTH /= 2.0
            elif event.unicode == '-':
                FRAME_LENGTH *= 2.0
            elif event.unicode == 'k':
                user.kill()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mx, my = event.pos
            new = Ent(mx, my, blockimg.get_width(), blockimg.get_height(), blockimg)
            level.add_obst(new)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dirn = vsub(event.pos, user.centre())
            user.speed = vscale(BOOST_SPEED/vnorm(dirn), dirn)

    pr = pygame.key.get_pressed()
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
        if user.jumping and user.jumping <= JUMP_ACCEL_LEN and pr[keys.JUMP]:
            sp[1] -= JUMP_ACCEL
            user.jumping += 1
        else:
            yaccel = GRAV_ACCEL
            if pr[keys.JUMP] and sp[1]<0:
                yaccel *= ((1 - GRAV_ACCEL_RAT_COEF) * (-sp[1]))**2
            sp[1] += GRAV_ACCEL
            user.jumping = False
    
    print "speed: %s,  posn: (%s,%s), grounded: %s" %\
        (user.speed, user.xpos, user.ypos, user.grounded)
    #print "plat: %s" % level.obsts[34]
    coll_move(user, level)

    # TODO: don't flip every frame
    #screen.fill(bgcolor)
    unblitted_rects = []
    for ghost in level.ghosts:
        ghost.unblit(screen, unblitted_rects)
    dirty_rects = unblitted_rects[:]
    for thing in [user] + level.obsts:
        thing.unblit(screen, unblitted_rects)
    for thing in level.obsts + [user]:
        thing.blitto(screen, unblitted_rects, dirty_rects)
    b4render = time.time()
    pygame.display.update(dirty_rects)
    level.ghosts = []

    # gather benchmark data
    after_render = time.time()
    frame_time = after_render - t0
    render_time = time.time() - b4render
    #print "render/frame: %sms,  %sms" % (render_time*1000, frame_time*1000)
    avg_render_time -= avg_render_time/(frame+1)
    avg_render_time += render_time/(frame+1)
    avg_frame_time  -= avg_frame_time/(frame+1)
    avg_frame_time  += frame_time/(frame+1)

    if after_render < t0 + FRAME_LENGTH:
        time.sleep(t0+FRAME_LENGTH - after_render)
