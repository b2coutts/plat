#!/usr/bin/env python2

from util import *
from level import level # TODO: remove

inf = float('inf')

def coll_move(ent, obsts, tstep=1.0):
    '''Move ent 1 for time t according to its speed/position, respecting
       collisions with the Ents in the list obsts'''
    print "\tcoll_move t=%s, ent=%s" % (tstep, ent)

    # detect collisions
    rec_t = tstep # time of the soonest collision
    rec_type = '-' # 'u' for up face, 'd' for down, 'l' left, 'r' right
    rec_obst = False
    for obst in obsts:
        # iterate over corners of ent
        # TODO: more accurate collision detection would use a more complex polygon
        sp = ent.speed
        for p1,p2 in [(ent.xpos, ent.ypos),\
                      (ent.xpos, ent.ypos+ent.height),\
                      (ent.xpos+ent.width, ent.ypos),\
                      (ent.xpos+ent.width, ent.ypos+ent.height)]:
            x1,y1,w,h = obst.get_rect()
            x2,y2 = x1+w, y1+h

            if sp[0] == 0:
                lb_hori = -inf if x1 < p1 < x2 else inf
                ub_hori = -lb_hori
            elif sp[0] > 0:
                lb_hori = (x1-p1)/sp[0]
                ub_hori = (x2-p1)/sp[0]
            else:
                lb_hori = (x2-p1)/sp[0]
                ub_hori = (x1-p1)/sp[0]

            if sp[1] == 0:
                lb_vert = -inf if y1 < p2 < y2 else inf
                ub_vert = -lb_vert
            elif sp[1] > 0:
                lb_vert = (y1-p2)/sp[1]
                ub_vert = (y2-p2)/sp[1]
            else:
                lb_vert = (y2-p2)/sp[1]
                ub_vert = (y1-p2)/sp[1]

            #if obst == level[-1]:
                #print '\tlbv is %s, y1=%s, p2=%s, sp[1]=%s' % (lb_vert, y1, p2, sp[1])

            t0 = max(lb_hori,lb_vert)
            # TODO: problem is that COLL_BUFFER as used here will be a buffer of
            # time, not space. Will be impossible to have a collision buffer if,
            # i.e., we only have inf/-inf values for when a speed type is 0
            if 0 <= t0 < min(rec_t, ub_hori, ub_vert) or\
               (t0 < 0 < min(ub_hori, ub_vert) and t0 < rec_t):
                if lb_hori >= lb_vert and sp[0] >= obst.speed[0]:
                    rtype = 'l'
                elif lb_hori >= lb_vert and sp[0] < obst.speed[0]:
                    rtype = 'r'
                elif lb_hori < lb_vert and sp[1] >= obst.speed[1]:
                    rtype = 'u'
                elif lb_hori < lb_vert and sp[1] < obst.speed[1]:
                    rtype = 'd'

                rec_type = rtype
                rec_t = t0
                rec_obst = obst

    # resolve collision detection; move to collision then slide along surface
    ent.xpos += ent.speed[0] * rec_t
    ent.ypos += ent.speed[1] * rec_t
    if rec_type in 'lr':
        ent.speed[0] = 0
    elif rec_type in 'ud':
        ent.speed[1] = 0
        if rec_type == 'u':
            ent.grounded = rec_obst

    print "\tend: rec_t=%s, rec_type=%s, ent=%s" % (rec_t, rec_type, ent)

    if rec_type != '-':
        coll_move(ent, obsts, tstep-max(0,rec_t))
