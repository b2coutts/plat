#!/usr/bin/env python2

import sys, pygame, time
from params import *

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

import keys, audio
from lvl1 import level
from Level import *
from Ent import *
from util import *
from collision import coll_move, blink


audio.init()

start_time = time.time()

userimgr = pygame.image.load("img/lilguy.png").convert_alpha()
userimgl = pygame.transform.flip(userimgr,1,0)
blockimg = pygame.image.load("img/block.png").convert()
waterimg = pygame.image.load("img/water.png").convert_alpha()
blinkimg = pygame.image.load("img/blink.png").convert_alpha()

userright= True
last_shot= -GUN_COOLDOWN
last_blink = -BLINK_COOLDOWN
def usersprite(usr):
    global userright
    if usr.speed[0] != 0:
        userright = usr.speed[0] > 0
    return userimgr if userright else userimgl
user = Ent(level.spawn[0], level.spawn[1], userimgr.get_width(),\
           userimgr.get_height(), usersprite)
user.level = level

def can_ground(usr, obst):
    return usr.right() >= obst.left() and\
           usr.left() <= obst.right() and\
           float_eq(usr.bottom(), obst.top())

# makes a temporary visual effect
def mk_effect(img, x, y, dur):
    end = frame + dur
    print 'target is %s' % end
    def beh(obst, level, user, frame):
        print 'cur is %s' % frame
        if frame >= end:
            print 'foobar'
            level.rm_obst(obst.level_idx)
    return Ent(x, y, img.get_width(), img.get_height(), img, solid=False, beh=beh)

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
        user.has_dash = True
        for obst in level.obsts:
            if can_ground(user, obst):
                user.grounded = obst
                break

    # update user dash
    if user.dashing:
        user.dashing = user.dashing - 1
        if not user.dashing:
            user.speed[0] = user.speed[0] * DASH_DECEL
            user.speed[1] = user.speed[1] * DASH_DECEL

    # update platform speeds
    level.tick(frame, user)
    #print "plat: %s" % level.obsts[-1]
    for obst in level.obsts:
        if obst.behaviour:
            obst.behaviour(obst, level, user, frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print '%s frames/%s sec. avg render/frame: %sms,  %sms' %\
                  (frame, time.time()-start_time, avg_render_time*1000,\
                   avg_frame_time*1000)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pr = pygame.key.get_pressed()
            if event.key == keys.JUMP and user.grounded:
                user.grounded = False
                user.has_dash = True
                user.jumping = 1
                audio.play(audio.sfx_jump)
            elif user.has_dash and not user.grounded and event.key == keys.DASH:
                user.speed[0] = user.speed[1] = 0
                if pr[keys.LEFT]:
                    user.speed[0] = user.speed[0] - 1
                if pr[keys.RIGHT]:
                    user.speed[0] = user.speed[0] + 1
                if pr[keys.UP]:
                    user.speed[1] = user.speed[1] - 1
                if pr[keys.DOWN]:
                    user.speed[1] = user.speed[1] + 1
                normalize(user.speed, DASH_SPEED)

                user.has_dash = False
                user.dashing  = DASH_DURATION
                audio.play(audio.sfx_dash)
            elif last_blink + BLINK_COOLDOWN <= frame and event.key == keys.BLINK:
                user.grounded = False
                user.speed[0] = user.speed[1] = 0
                dirn = [0,0]

                if pr[keys.LEFT]:
                    dirn[0] = dirn[0] - 1
                if pr[keys.RIGHT]:
                    dirn[0] = dirn[0] + 1
                if pr[keys.UP]:
                    dirn[1] = dirn[1] - 1
                if pr[keys.DOWN]:
                    dirn[1] = dirn[1] + 1
                normalize(dirn)

                oldx, oldy = user.xpos, user.ypos
                blink(user, level, dirn, BLINK_DIST)

                w,h = user.width, user.height
                xmin, xmax = int(min(user.xpos, oldx)), int(max(user.xpos, oldx))
                ymin, ymax = int(min(user.ypos, oldy)), int(max(user.ypos, oldy))
                linesfc = pygame.Surface((xmax-xmin+2, ymax-ymin+2), flags=pygame.SRCALPHA)
                linesfc.fill((0,0,0,0))
                line = pygame.draw.line(linesfc, (0,0,255),\
                                        [int(oldx) - xmin, int(oldy) - ymin],\
                                        [int(user.xpos) - xmin, int(user.ypos) - ymin], 3)
                level.add_obst(mk_effect(linesfc, min(oldx, user.xpos) + w/2, min(oldy, user.ypos) + h/2, 10))
                level.add_obst(mk_effect(blinkimg, oldx, oldy, 10))
                level.add_obst(mk_effect(blinkimg, user.xpos, user.ypos, 10))

                audio.play(audio.sfx_blink)
                last_blink = frame
            elif event.key == keys.SUICIDE:
                user.kill()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if MOUSE_MODE == 1:
                if last_shot+GUN_COOLDOWN <= frame:
                    spawn = [user.xpos + (14 if userright else 0), user.ypos+5]
                    dirn  = vsub(event.pos, spawn)
                    spd   = vscale(BULLET_SPEED/vnorm(dirn), dirn)
                    bullet = mkprojectile(spawn, 1, 1, spd, waterimg, False)
                    bullet.solid = False
                    bullet.spec['fragile'] = True
                    level.add_obst(bullet)
                    last_shot = frame
                    audio.play(audio.sfx_water)

        # debug controls
        if DEBUG:
            if event.type == pygame.KEYDOWN:
                if event.unicode == '+':
                    FRAME_LENGTH /= 2.0
                elif event.unicode == '-':
                    FRAME_LENGTH *= 2.0
                elif event.unicode == '0':
                    MOUSE_MODE = 0
                elif event.unicode == '1':
                    MOUSE_MODE = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if MOUSE_MODE == 0:
                    dirn = vsub(event.pos, user.centre())
                    user.speed = vscale(BOOST_SPEED/vnorm(dirn), dirn)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = event.pos
                new = Ent(mx, my, blockimg.get_width(), blockimg.get_height(),\
                          blockimg)
                level.add_obst(new)

    pr = pygame.key.get_pressed()
    sp = user.speed
    if user.grounded:
        sp[0] = user.grounded.speed[0]
        sp[1] = user.grounded.speed[1]
        if pr[keys.LEFT]:
            sp[0] -= RUN_SPEED
        elif pr[keys.RIGHT]:
            sp[0] += RUN_SPEED
    # do not accelerate if in the middle of a dash
    elif not user.dashing:
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
        if user.jumping and user.jumping <= JUMP_ACCEL_LEN:
            if pr[keys.JUMP]:
                sp[1] -= JUMP_ACCEL
                user.jumping += 1
            else:
                sp[1] = 0
                user.jumping = False
        else:
            sp[1] += GRAV_ACCEL
            user.jumping = False
    
    print "Frame %s"  % frame
    print "num_obsts: %s" % len(level.obsts)
    print "speed: %s,  posn: (%s,%s), has_dash: %s, dashing: %s, blinkcd: %s\n%s" %\
        (user.speed, user.xpos, user.ypos, user.has_dash, user.dashing,
         max(0, last_blink + BLINK_COOLDOWN - frame), user.grounded)
    #print "plat: %s" % level.obsts[-1]
    coll_move(user, level)

    # TODO: don't flip every frame
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
