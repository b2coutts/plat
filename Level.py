#!/usr/bin/env python2

import math, pygame, sys

from Ent import Ent
from util import *
import params, audio

blockimg = pygame.image.load("img/block.png").convert()
kbimg    = pygame.image.load("img/kb.png").convert()
startimg = pygame.image.load("img/start.png").convert_alpha()
cpimg    = pygame.image.load("img/cp.png").convert_alpha()
finimg   = pygame.image.load("img/finish.png").convert_alpha()

class Level:
    # obsts : list of obstacle Ents
    # ticks : list of tick functions tick(level, frame, user)
    # ghosts: list of rects that are being deleted
    # spawn : current user spawn point
    
    def __init__(self, spawn):
        self.obsts  = []
        self.ticks  = []
        self.ghosts = []
        self.spawn  = spawn
        self.add_obst(mkcheckpoint(spawn[0], spawn[1], startimg))

    def tick(self, frame, user):
        for tick in self.ticks:
            tick(self, frame, user)

    def add_obst(self, obst):
        obst.level     = self
        obst.level_idx = len(self.obsts)
        self.obsts.append(obst)

    def rm_obst(self, idx):
        self.ghosts.append(self.obsts[idx])
        self.obsts[idx].xpos = self.obsts[idx].ypos = float('inf')
        del self.obsts[idx]
        for i in range(idx,len(self.obsts)):
            self.obsts[i].level_idx -= 1

    def add_tick(self, tick):
        self.ticks.append(tick)

# makes a standard platform
def mkplat(xp, yp, w, h, spd=[0,0], img=blockimg, beh=False, deadly=False,\
           solid=True, killsfx=audio.sfx_died):
    right = w*img.get_width()
    bottom = h*img.get_height()
    platimg = pygame.Surface((right, bottom))
    x = y = 0
    while x < right:
        if x > right - img.get_width():
            x = right - img.get_width()
        while y < bottom:
            if y > bottom - img.get_height():
                y = bottom - img.get_height()
            platimg.blit(img, (x,y))
            y += img.get_height()
        y = 0
        x += img.get_width()
    return Ent(xp, yp, w*img.get_width(), h*img.get_height(), platimg.convert(),\
               spd[:], beh=beh, deadly=deadly, solid=solid, killsfx=killsfx)

# makes a platform whose pos oscillates between a and b, with speed magnitude s
def mkosc(a, b, w, h, s, img=blockimg, deadly=False):
    def beh(plat, level, user, frame):
        # reverse direction if necessary
        if plat.atob:
            if vdot(vsub(b,a), vsub([plat.xpos,plat.ypos], b)) > EPSILON:
                plat.atob = False
        else:
            if vdot(vsub(b,a), vsub([plat.xpos,plat.ypos], a)) < EPSILON:
                plat.atob = True

        dirn = vsub(b,a) if plat.atob else vsub(a,b)
        plat.speed = vscale(s/vnorm(dirn), dirn)
    plat = mkplat(a[0], a[1], w, h, img=img, beh=beh, deadly=deadly)
    plat.atob = True
    return plat

# makes a platforms which moves in a circle of radius r, centred at c, with
# period T, initial angle theta, initial direction CW if cw else CCW.
# TODO: should the centre of the platform have distance r from c, or the UL
# corner?
def mkcircler(c, r, w, h, T, theta, cw, img=blockimg, deadly=False,\
              solid=True):
    x,y = vadd(c, vscale(r, [math.cos(theta), math.sin(theta)]))
    def beh(plat, level, user, frame):
        f = frame % T
        angle = theta + (f*2*math.pi/T)

        plat.speed = vscale(2*math.pi*r/T, [-math.sin(angle),\
                                            (1 if cw else -1)*math.cos(angle)])
    return mkplat(x,y,w,h,[0,0], img, beh, deadly, solid)

# makes a projectile shooter (tick function)
def mkshooter(spawn, w, h, spd, period, dur, img, deadly, killsfx=audio.sfx_died):
    def tick(level, frame, user):
        if frame%period == 0:
            def beh(obst, level2, user, frame2):
                if frame2-frame >= dur:
                    level.rm_obst(obst.level_idx)
            level.add_obst(mkplat(spawn[0], spawn[1], w, h, spd, img, beh,\
                           deadly, killsfx=killsfx))
    return tick

# makes a checkpoint
def mkcheckpoint(x, y, img=cpimg):
    def beh(obst, level, user, frame):
        if obst.get_rect().colliderect(user.get_rect()):
            if level.spawn != [x,y]:
                audio.play(audio.sfx_cp)
            level.spawn = [x,y]
    return Ent(x, y, img.get_width(), img.get_height(), img, beh=beh,\
               solid=False)

# makes a finish flag
def mkfinish(x, y):
    def beh(obst, level, user, frame):
        if obst.get_rect().colliderect(user.get_rect()):
            # TODO: winning code
            print 'You win!'
    return Ent(x, y, finimg.get_width(), finimg.get_height(), finimg, beh=beh,\
               solid=False)
