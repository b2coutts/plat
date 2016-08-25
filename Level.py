#!/usr/bin/env python2

import math, pygame

from Ent import Ent
import params

blockimg = pygame.image.load("img/block.png").convert()
kbimg    = pygame.image.load("img/kb.png").convert()

class Level:
    # obsts : list of obstacle Ents
    # ticks : list of tick functions tick(level, frame)
    # ghosts: list of rects that are being deleted
    # spawn : current user spawn point
    
    def __init__(self, spawn):
        self.obsts  = []
        self.ticks  = []
        self.ghosts = []
        self.spawn  = spawn

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
def mkplat(xp, yp, w, h, spd=[0,0], img=blockimg, beh=False, deadly=False):
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
    return Ent(xp, yp, w*img.get_width(), h*img.get_height(),\
               platimg.convert(), spd[:], beh=beh, deadly=deadly)

# makes a platform whose pos oscillates between a and b, with speed magnitude s
def mkosc(a, b, w, h, s, img=blockimg, deadly=False):
    def beh(plat, frame):
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

# makes a projectile shooter (tick function)
def mkshooter(spawn, w, h, spd, period, dur, img, deadly):
    def tick(level, frame, user):
        def beh(obst, frame2):
            if frame2-frame >= dur:
                level.rm_obst(obst.level_idx)
        if frame%period == 0:
            level.add_obst(mkplat(spawn[0], spawn[1], w, h, spd, img, beh,\
                                  deadly))
    return tick
