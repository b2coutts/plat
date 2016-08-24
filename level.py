#!/usr/bin/env python2

from Ent import *
import params

bwidth = 20
w,h = params.SCREEN_SIZE

blockimg = pygame.image.load("img/block.png")

def mover_beh(plat, frame):
    if (frame+1)%(60*5) == 0:
        plat.speed[0] *= -1

def elev_beh(plat, frame):
    if (frame+1)%(60*4) == 0:
        plat.speed[0] *= -1
        plat.speed[1] *= -1

b_top   = Ent(-bwidth, -bwidth, w + 2*bwidth, bwidth)
b_left  = Ent(-bwidth, -bwidth, bwidth, h + 2*bwidth)
b_right = Ent(w, -bwidth, bwidth, h + 2*bwidth)
b_bot   = Ent(-bwidth, h, w + 2*bwidth, bwidth)
plat   = Ent(200, 320, 40, 20, blockimg)
mover   = Ent(200, 300, 110, 20, blockimg, [1,0], beh=mover_beh)
elevator = Ent(50, 350, 100, 20, blockimg, [1,-1], beh=elev_beh)

# TODO: this should probably just be a class or something
level = [b_top, b_left, b_right, b_bot, plat, mover, elevator]
