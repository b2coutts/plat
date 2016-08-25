#!/usr/bin/env python2

import math

from Ent import *
import params

blockimg = pygame.image.load("img/block.png").convert()
kbimg    = pygame.image.load("img/kb.png").convert()

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

# platform whose pos oscillates between a and b, with speed magnitude s
def mkosc(a, b, w, h, s, img=blockimg, deadly=False):
    def beh(plat, frame):
        # reverse direction if necessary
        if plat.atob:
            if vdot(vsub(b,a), vsub([plat.xpos,plat.ypos], b)) > 0:
                plat.atob = False
        else:
            if vdot(vsub(b,a), vsub([plat.xpos,plat.ypos], a)) < 0:
                plat.atob = True

        dirn = vsub(b,a) if plat.atob else vsub(a,b)
        plat.speed = vscale(s/vnorm(dirn), dirn)
    plat = mkplat(a[0], a[1], w, h, img=img, beh=beh, deadly=deadly)
    plat.atob = True
    return plat

bwidth = 20
w,h = params.SCREEN_SIZE

def circle_beh(plat,frame):
    t = frame * (2*math.pi)/(60*10.0)
    plat.speed = [math.cos(t), math.sin(t)]

border  = [Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth),\
           Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth),\
           Ent(w, -bwidth, bwidth, h + 2*bwidth),\
           Ent(-bwidth, h, w + 2*bwidth, bwidth)]
vborder = [mkplat(0, 0, 40, 1), mkplat(0, 0, 1, 30), mkplat(0, 580, 40, 1),\
           mkplat(780, 0, 1, 30)]
lavapit = [mkplat(170, 420, 1, 8), mkplat(290, 420, 1, 8), mkplat(170, 560, 7, 1),\
           mkplat(190, 480, 5, 4, img=kbimg, deadly=True)]
elev    = [mkosc((90,560), (90,420), 4, 1, 1.5)]
laggers = [mkosc((90,20+30*x), (490,20+30*x), 4, 1, x/2.0) for x in range(20)]
circle  = [mkplat(500, 200, 5, 1, beh=circle_beh)]
weird   = [mkosc((90,560), (230.023, 420.432), 4, 1, 1.5)]


# TODO: this should probably just be a class or something
#level = border + vborder + lavapit + elev + circle
level = border + vborder + weird + circle
