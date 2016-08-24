#!/usr/bin/env python2

import sys
from util import *
from level import level # TODO: remove

inf = float('inf')

# TODO: possible numerical issue when stepping obsts forward by awkward amounts
def coll_move(ent, obsts, tstep=1.0, killzero = False):
    '''Move ent 1 for time t according to its speed/position, respecting
       collisions with the Ents in the list obsts. Also advances obsts
       forward'''
    print "\tcoll_move t=%s, ent=%s" % (tstep, ent)

    # detect collisions
    rec_t = tstep # time of the soonest collision
    rec_type = '-' # 'u' for up face, 'd' for down, 'l' left, 'r' right
    rec_obst = False
    for obst in obsts:
        # iterate over corners of ent
        # TODO: more accurate collision detection would use a more complex polygon
        for p1,p2 in [(ent.xpos, ent.ypos),\
                      (ent.xpos, ent.ypos+ent.height),\
                      (ent.xpos+ent.width, ent.ypos),\
                      (ent.xpos+ent.width, ent.ypos+ent.height)]:
            a1,a2,w,h = obst.get_rect()
            b1,b2 = a1+w, a2+h
            sp = vsub(ent.speed, obst.speed)

            if sp[0] == 0:
                lb_hori = -inf if a1 < p1 < b1 else inf
                ub_hori = -lb_hori
            elif sp[0] > 0:
                lb_hori = (a1-p1)/sp[0]
                ub_hori = (b1-p1)/sp[0]
            else:
                lb_hori = (b1-p1)/sp[0]
                ub_hori = (a1-p1)/sp[0]

            if sp[1] == 0:
                lb_vert = -inf if a2 < p2 < b2 else inf
                ub_vert = -lb_vert
            elif sp[1] > 0:
                lb_vert = (a2-p2)/sp[1]
                ub_vert = (b2-p2)/sp[1]
            else:
                lb_vert = (b2-p2)/sp[1]
                ub_vert = (a2-p2)/sp[1]

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
    for thing in [ent] + obsts:
        thing.xpos += thing.speed[0] * rec_t
        thing.ypos += thing.speed[1] * rec_t
    if rec_type in 'lr':
        ent.speed[0] = rec_obst.speed[0]
    elif rec_type in 'ud':
        ent.speed[1] = rec_obst.speed[1]
        if rec_type == 'u':
            ent.grounded = rec_obst

    print "\tend: rec_t=%s, rec_type=%s, ent=%s" % (rec_t, rec_type, ent)

    if rec_t == 0.0 and killzero:
        print "User died!"
        ent.kill()
        for obst in obsts:
            obst.xpos += obst.speed[0] * tstep
            obst.ypos += obst.speed[1] * tstep
        return

    if rec_t < tstep:
        coll_move(ent, obsts, tstep-max(0,rec_t), rec_t == 0.0)
