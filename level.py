#!/usr/bin/env python2

from Ent import *
import params

bwidth = 20
w,h = params.SCREEN_SIZE

blockimg = pygame.image.load("img/block.png")
kbimg    = pygame.image.load("img/kb.png")

def mkplat(x, y, w, h, spd=[0,0], img=blockimg, beh=False, deadly=False):
    return Ent(x, y, w*img.get_width(), h*img.get_height(), img, spd[:],\
               beh=beh, deadly=deadly)

# platform whose pos oscillates between a and b, with speed magnitude s
def mkosc(a, b, w, h, s, img=blockimg, deadly=False):
    def beh(plat, frame):
        print "beh: init %s" % plat
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

border  = [Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth),\
           Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth),\
           Ent(w, -bwidth, bwidth, h + 2*bwidth),\
           Ent(-bwidth, h, w + 2*bwidth, bwidth)]
lavapit = [mkplat(250, 240, 1, 8), mkplat(370, 240, 1, 8), mkplat(250, 380, 7, 1),\
           mkplat(270, 300, 5, 4, img=kbimg, deadly=True)]
elev    = [mkosc((170,380), (170,240), 4, 1, 1.5)]


# TODO: this should probably just be a class or something
level = border + lavapit + elev
