#!/usr/bin/env python2

import sys
from util import *

inf = float('inf')

# TODO: possible numerical issue when stepping obsts forward by awkward amounts
def coll_move(ent, level, tstep=1.0, zeros = 0):
    '''Move ent 1 for time t according to its speed/position, respecting
       collisions with the Ents in level.obsts. Also advances obsts forward'''
    #print "coll_move t=%s, ent=%s" % (tstep, ent)

    # detect collisions
    rec_t = tstep # time of the soonest collision
    rec_type = '-' # 'u' for up face, 'd' for down, 'l' left, 'r' right
    rec_obst = False
    c1,c2,d1,d2 = ent.left(), ent.top(), ent.right(), ent.bottom()
    for obst in level.obsts:
        if not obst.solid:
            continue
        a1,a2,b1,b2 = obst.left(), obst.top(), obst.right(), obst.bottom()
        sp = vsub(ent.speed, obst.speed)

        if float_eq(sp[0],0):
            # TODO: is this check numerically bad?
            lb_hori = -inf if d1>a1 and c1<b1 else inf
            ub_hori = -lb_hori
        elif sp[0] > 0:
            lb_hori = (a1-d1)/sp[0]
            ub_hori = (b1-c1)/sp[0]
        else:
            lb_hori = (b1-c1)/sp[0]
            ub_hori = (a1-d1)/sp[0]

        if float_eq(sp[1],0):
            lb_vert = -inf if d2>a2 and c2<b2 else inf
            ub_vert = -lb_vert
        elif sp[1] > 0:
            lb_vert = (a2-d2)/sp[1]
            ub_vert = (b2-c2)/sp[1]
        else:
            lb_vert = (b2-c2)/sp[1]
            ub_vert = (a2-d2)/sp[1]

        t0 = max(lb_hori,lb_vert)
        # TODO: problem is that COLL_BUFFER as used here will be a buffer of
        # time, not space. Will be impossible to have a collision buffer if,
        # i.e., we only have inf/-inf values for when a speed type is 0
        if 0 <= t0 < min(rec_t, ub_hori, ub_vert):
            if lb_hori >= lb_vert and sp[0] >= 0:
                rtype = 'l'
            elif lb_hori >= lb_vert and sp[0] < 0:
                rtype = 'r'
            elif lb_hori < lb_vert and sp[1] >= 0:
                rtype = 'u'
            elif lb_hori < lb_vert and sp[1] < 0:
                rtype = 'd'
            else:
                print "No rtype!!!"
                sys.exit()

            rec_type = rtype
            rec_t = t0
            rec_obst = obst

    # resolve collision detection; move to collision then slide along surface
    for thing in [ent] + level.obsts:
        thing.xpos += thing.speed[0] * rec_t
        thing.ypos += thing.speed[1] * rec_t
    if rec_type in 'lr':
        ent.speed[0] = rec_obst.speed[0]
    elif rec_type in 'ud':
        ent.speed[1] = rec_obst.speed[1]
        if rec_type == 'u':
            ent.grounded = rec_obst

    #print "\tend: rec_t=%s, rec_type=%s, ent=%s" % (rec_t, rec_type, ent)

    if (float_eq(rec_t,0.0) and zeros >= 2) or (rec_obst and rec_obst.deadly):
        print "User died!"
        ent.kill(rec_obst.killsfx)
        for obst in level.obsts:
            obst.xpos += obst.speed[0] * tstep
            obst.ypos += obst.speed[1] * tstep
        return

    if tstep - rec_t > EPSILON:
        newzeros = zeros+1 if float_eq(rec_t,0.0) else 0
        coll_move(ent, level, tstep-max(0,rec_t), newzeros)
